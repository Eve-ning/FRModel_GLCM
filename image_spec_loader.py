from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Callable

import numpy as np
from tqdm import tqdm

from conf import FILE_INFO


@dataclass
class ImageSpecLoader:
    channel_labels: List[str] = field(default_factory=lambda: [])
    ar_normalized: np.ndarray = None

    @staticmethod
    def preprocess(im_path: Path,
                   bits: int,
                   channels: int,
                   read_method: Callable) -> np.ndarray:
        """ Adjusts the image such that it's acceptable by concat

        Parameters
        ----------
        im_path
             Path to image
        bits
             Number of bits of the image
        channels
             Channels to yield. If None, then we extend a channel
        read_method
             Callable to read the image

        Returns
        -------
        np.ndarray
            Normalized array with ndim == 3
        """
        normalized = read_method(im_path) / (2 ** bits)
        return normalized[..., np.newaxis if channels is None else channels]

    @staticmethod
    def load(im_paths: List[Path],
             normalize_per_pixel: bool = False) -> ImageSpecLoader:
        """ Loads the Images, joins and normalizes them

        Parameters
        ----------
        im_paths
            Paths to the images
        normalize_per_pixel
            Whether to normalize by pixel.

        Returns
        -------
        ImageSpecLoader
            An instance with `channel_labels` and normalized array
            `ar_normalized`.
        """
        data = ImageSpecLoader()
        ars = []

        for im_path in tqdm(im_paths, desc="Reading Files"):
            # We get the details per file
            info = FILE_INFO[im_path.name]
            # We preprocess according to these details
            ar = data.preprocess(im_path,
                                 bits=info['bits'],
                                 channels=info['channels'],
                                 read_method=info['read_method'])

            # Append channel names
            data.channel_labels.extend(info['channel_names'])

            ars.append(ar)

        data.ar_normalized = np.concatenate(ars, axis=2)

        if normalize_per_pixel:
            data.ar_normalized = \
                ImageSpecLoader.normalize_per_pixel(data.ar_normalized)

        data._check_valid()

        return data

    @staticmethod
    def normalize_per_pixel(ar: np.ndarray, axis=2):
        """ Normalizes the image by pixel.

        Notes
        -----
        Normalizing the image can cause consistently dimmer channels to
        diminish to 0, likewise with brighter channels to saturate to 1.

        Parameters
        ----------
        ar
            Array to normalize.
        axis
            Axis to normalize, default the channel axis.

        Returns
        -------
        np.ndarray
            Normalized Image

        """
        minimum = np.min(ar, axis=axis)[..., np.newaxis]
        maximum = np.max(ar, axis=axis)[..., np.newaxis]
        return (ar - minimum) / (maximum - minimum)

    def _check_valid(self) -> None:
        """ Performs a final check on the preprocessed data """

        assert (i := self.ar_normalized.shape[-1]) == \
               (j := len(self.channel_labels)), \
            f"Unexpected mismatch in number of labels and channels." \
            f"{i} != {j}"
        assert (i := np.nanmax(self.ar_normalized)) <= 1, \
            f"Unexpected datapoint exceeds 1 despite normalization. {i}"
