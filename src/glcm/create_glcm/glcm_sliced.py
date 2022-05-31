from __future__ import annotations

import numpy as np
import pandas as pd
import pickle
import shutil
from pathlib import Path
from typing import Dict

from conf import INFO_MD_FILE
from glcm_cupy import GLCM
from glcm_cupy.glcm_base import GLCMBase


def glcm_sliced(glcm: GLCMBase,
                ar: np.ndarray,
                bounds_path: Path,
                save_dir: Path = Path(""),
                scale_division: int = 1,
                minmax: bool = False,
                pixel_norm: bool = False,
                ):
    """ Slices the Image and runs GLCM on it

    Examples
    --------

    >>> glcm_sliced(ar, Path("bounds.csv"), scale_division=5)

    Parameters
    ----------
    glcm
        GLCM Instance to use for glcm
    ar
        Array to slice
    bounds_path
        The file path to the bounds
    scale_division
        The division to downscale the image to. Must be an integer.
    save_dir
        Path to export the slice to
    minmax
        Whether to minmax scale each tree
    pixel_norm 
        Whether to pixel normalize each tree

    Returns
    -------
    Dict[str, List[np.ndarray]]
        Keys of the same dictionary and sliced np.ndarray
    """

    # Rescale the image and bounds
    assert type(scale_division) == int, "Scale division must be integer!"

    ar = ar[::scale_division, ::scale_division]

    if minmax:
        ar = minmax_ar(ar)

    save_dir.mkdir(parents=True, exist_ok=True)

    for ix, bound in pd.read_csv(bounds_path, sep="|").iterrows():
        name: str = bound['name']
        # Check if NPZ already exists
        save_dump = save_dir / f"{name}_{ix}.npz"
        if save_dump.exists():
            print(f"{name}_{ix} exists, skipping")
            continue

        bound[['y0', 'y1', 'x0', 'x1']] //= scale_division

        ar_slice = ar[bound['y0']:bound['y1'], bound['x0']:bound['x1']]

        if pixel_norm:
            ar_slice = glcm_pixel_norm(ar_slice)

        g = glcm.run(ar_slice).astype(np.float16)

        if isinstance(glcm, GLCM):
            crop = glcm.step_size + glcm.radius
            g = np.concatenate(
                [ar_slice[crop:-crop, crop:-crop, :, np.newaxis], g],
                axis=3
            )

        with open(save_dump, "wb") as f:
            pickle.dump(g, f)

        copy_info_md(save_dir)
        break


def glcm_pixel_norm(ar: np.ndarray):
    return ar / ar.sum(axis=2)[..., np.newaxis]


def minmax_ar(ar: np.ndarray):
    return (ar - np.nanmin(ar)) / (np.nanmax(ar) - np.nanmin(ar))


def copy_info_md(save_dir):
    shutil.copy(INFO_MD_FILE, save_dir)
