from __future__ import annotations

import numpy as np
import pickle
from abc import abstractmethod
from dataclasses import dataclass, field
from matplotlib import pyplot as plt
from pathlib import Path
from tqdm import tqdm
from typing import List, Tuple

from conf import OUTPUT_DIR_GLCM, OUTPUT_DIR_GLCM_CROSS
from glcm.create_report.conf import FEATURES, NO_OF_FEATURES, CHANNELS, \
    CHANNELS_CROSS, HIST_BINS, STACKED_HIST_ALPHA, GLCM_STACK_HIST_FIGSIZE, \
    GLCM_HIST_FIGSIZE, GLCM_IM_FIGSIZE, GLCM_CROSS_STACK_HIST_FIGSIZE, \
    GLCM_CROSS_HIST_FIGSIZE, GLCM_CROSS_IM_FIGSIZE
from glcm.upload import GCS


@dataclass
class Plot:
    tree_path: Path
    gcs: GCS
    channel_names: List[str]
    figsize: Tuple[int, int]
    fig: plt.Figure = field(init=False, default=None)
    axes: List[List[plt.Axes]] = field(init=False, default=None)

    def init_plot(self):
        self.fig, self.axes = plt.subplots(
            len(self.channel_names), NO_OF_FEATURES,
            figsize=self.figsize
        )

    @property
    def exists(self) -> bool:
        return self.gcs.exists_on_cloud(self.save_path)

    def plot(self, tree: np.ndarray, channel: int, feature: int,
             tree_name: str):
        if self.fig is None:
            self.init_plot()
        ax = self.axes[channel, feature]
        self.plot_fn(ax, tree[..., channel, feature],
                     channel=channel, feature=feature, tree_name=tree_name)

        ax.set_yticks([])
        ax.set_xticks([])
        if channel == 0:
            ax.set_title(FEATURES[feature])
        if feature == 0:
            ax.set_ylabel(self.channel_names[channel],
                          rotation='horizontal', ha='right')

    @abstractmethod
    def plot_fn(self, ax: plt.Axes, tree: np.ndarray, **kwargs):
        ...

    def save(self):
        self.fig.savefig(self.save_path)
        plt.close(self.fig)

    @property
    @abstractmethod
    def save_path(self):
        ...

    def __bool__(self):
        return self.exists


@dataclass
class StackedHistPlot(Plot):

    def init_plot(self):
        super().init_plot()
        self.fig.subplots_adjust(right=0.88)

    def save(self):
        self.fig.legend()
        super().save()

    @property
    def save_path(self) -> Path:
        return self.tree_path / "stacked_hist.jpg"

    def plot_fn(self, ax: plt.Axes, tree: np.ndarray, **kwargs):
        ax.hist(
            tree.flatten(), bins=HIST_BINS, alpha=STACKED_HIST_ALPHA,
            density=True,
            label=kwargs['tree_name'] if
            kwargs['channel'] + kwargs['feature'] == 0 else None
        )


@dataclass
class ImagePlot(Plot):

    def save(self):
        self.fig.tight_layout()
        super().save()

    @property
    def save_path(self) -> Path:
        return Path(self.tree_path.as_posix() + "_image.jpg")

    def plot_fn(self, ax: plt.Axes, tree: np.ndarray, **kwargs):
        ax.imshow(tree)


@dataclass
class HistPlot(Plot):

    def save(self):
        self.fig.tight_layout()
        super().save()

    @property
    def save_path(self) -> Path:
        return Path(Path(self.tree_path.as_posix() + "_hist.jpg"))

    def plot_fn(self, ax: plt.Axes, tree: np.ndarray, **kwargs):
        ax.hist(tree.flatten(), bins=HIST_BINS)


@dataclass
class Report:
    channel_names: List[str]
    output_dir: Path
    stack_hist_figsize: Tuple[int, int]
    hist_figsize: Tuple[int, int]
    im_figsize: Tuple[int, int]

    gcs = GCS()

    @property
    def set_paths(self) -> List[Path]:
        # noinspection PyTypeChecker
        return np.unique(
            [p.parent for p in Path(self.output_dir).glob("**/*.npz")]
        ).tolist()

    def create_report(self):

        for set_path in self.set_paths:
            tree_paths = list(set_path.glob("*.npz"))
            stack_hist_plt = StackedHistPlot(
                set_path, self.gcs, self.channel_names,
                figsize=self.stack_hist_figsize
            )
            t = tqdm(tree_paths)
            for tree_path in t:
                tree_path: Path
                t.set_description(f"Report {tree_path.stem}")
                im_plt = ImagePlot(tree_path, self.gcs, self.channel_names,
                                   self.im_figsize)
                hist_plt = HistPlot(tree_path, self.gcs, self.channel_names,
                                    self.hist_figsize)
                tree_name = tree_path.stem.split("_")[0]

                if stack_hist_plt and im_plt and hist_plt: continue

                with open(tree_path, "rb") as f:
                    tree = pickle.load(f)

                for f_ix in range(NO_OF_FEATURES):
                    for ch_ix in range(len(self.channel_names)):
                        plt_args = tree, ch_ix, f_ix, tree_name
                        if not hist_plt:
                            hist_plt.plot(*plt_args)
                        if not im_plt:
                            im_plt.plot(*plt_args)
                        if not stack_hist_plt:
                            stack_hist_plt.plot(*plt_args)

                if not hist_plt: hist_plt.save()
                if not im_plt: im_plt.save()

            if not stack_hist_plt: stack_hist_plt.save()
            plt.close('all')


def create_report_glcm():
    Report(
        channel_names=CHANNELS,
        output_dir=OUTPUT_DIR_GLCM,
        stack_hist_figsize=GLCM_STACK_HIST_FIGSIZE,
        hist_figsize=GLCM_HIST_FIGSIZE,
        im_figsize=GLCM_IM_FIGSIZE,

    ).create_report()


def create_report_glcm_cross():
    Report(
        channel_names=CHANNELS_CROSS,
        output_dir=OUTPUT_DIR_GLCM_CROSS,
        stack_hist_figsize=GLCM_CROSS_STACK_HIST_FIGSIZE,
        hist_figsize=GLCM_CROSS_HIST_FIGSIZE,
        im_figsize=GLCM_CROSS_IM_FIGSIZE,
    ).create_report()
