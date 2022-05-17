from __future__ import annotations

import numpy as np
import pickle
from abc import abstractmethod
from dataclasses import dataclass, field
from matplotlib import pyplot as plt
from pathlib import Path
from tqdm import tqdm
from typing import List, Tuple

from conf import CHANNELS, FEATURES, NO_OF_FEATURES, NO_OF_CHANNELS, OUTPUT_DIR


@dataclass
class Plot:
    tree_path: Path
    figsize: Tuple[int, int] = (20, 20)
    fig: plt.Figure = field(init=False, default=None)
    axes: plt.Axes = field(init=False, default=None)

    def init_plot(self):
        self.fig, self.axes = plt.subplots(
            NO_OF_CHANNELS, NO_OF_FEATURES,
            figsize=self.figsize
        )

    @property
    def exists(self):
        return self.save_path.exists()

    def plot(self, tree: np.ndarray, channel: int, feature: int):
        if self.fig is None:
            self.init_plot()
        ax = self.axes[channel, feature]
        self.plot_fn(ax, tree[..., channel, feature])

        ax.set_yticks([])
        ax.set_xticks([])
        if channel == 0:
            ax.set_title(FEATURES[feature])
        if feature == 0:
            ax.set_ylabel(CHANNELS[channel], rotation='horizontal', ha='right')

    @abstractmethod
    def plot_fn(self, ax: plt.Axes, tree: np.ndarray):
        ...

    @property
    @abstractmethod
    def save_path(self) -> Path:
        ...

    def save(self):
        self.fig.savefig(self.save_path)
        plt.close(self.fig)

    def __bool__(self):
        return self.exists


@dataclass
class StackedHistPlot(Plot):
    @property
    def save_path(self) -> Path:
        return self.tree_path / "stacked_hist.jpg"

    def plot_fn(self, ax: plt.Axes, tree: np.ndarray):
        ax.hist(tree.flatten(), bins=100, alpha=0.3, density=True)


@dataclass
class ImagePlot(Plot):
    @property
    def save_path(self) -> Path:
        return Path(self.tree_path.as_posix() + "_image.jpg")

    def plot_fn(self, ax: plt.Axes, tree: np.ndarray):
        ax.imshow(tree)


@dataclass
class HistPlot(Plot):
    @property
    def save_path(self) -> Path:
        return Path(self.tree_path.as_posix() + "_hist.jpg")

    def plot_fn(self, ax: plt.Axes, tree: np.ndarray):
        ax.hist(tree.flatten())


@dataclass
class Report:
    output_dir: Path = OUTPUT_DIR

    @property
    def set_paths(self) -> List[Path]:
        # noinspection PyTypeChecker
        return np.unique(
            [p.parent for p in Path(self.output_dir).glob("**/*.npz")]
        ).tolist()

    def create_report(self):
        for set_path in self.set_paths:
            tree_paths = list(set_path.glob("*.npz"))
            stack_hist_plt = StackedHistPlot(set_path)
            for tree_path in tqdm(tree_paths, desc=set_path.name):
                im_plt = ImagePlot(tree_path, figsize=(20, 20))
                hist_plt = HistPlot(tree_path, figsize=(15, 10))

                if stack_hist_plt and im_plt and hist_plt: continue

                with open(tree_path, "rb") as f:
                    tree = pickle.load(f)

                for f_ix in range(NO_OF_FEATURES):
                    for ch_ix in range(NO_OF_CHANNELS):
                        if not hist_plt:
                            hist_plt.plot(tree, ch_ix, f_ix)
                        if not im_plt:
                            im_plt.plot(tree, ch_ix, f_ix)
                        if not stack_hist_plt:
                            stack_hist_plt.plot(tree, ch_ix, f_ix)

                if not hist_plt: hist_plt.save()
                if not im_plt: im_plt.save()

            if not stack_hist_plt: stack_hist_plt.save()
            plt.close('all')

