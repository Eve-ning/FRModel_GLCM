from __future__ import annotations

import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from typing import Dict

from glcm_cupy import *


def glcm_sliced(glcm: GLCM,
                ar: np.ndarray,
                bounds_path: Path,
                save_file_path: Path = Path(""),
                scale_division: int = 1
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

    Returns
    -------
    Dict[str, List[np.ndarray]]
        Keys of the same dictionary and sliced np.ndarray
    """

    output = {}

    # Rescale the image and bounds
    assert type(scale_division) == int, "Scale division must be integer!"
    ar = ar[::scale_division, ::scale_division]

    for ix, bound in pd.read_csv(bounds_path, sep="|").iterrows():
        name = bound['name']

        # This will create a save file for individual trees
        save_file_path_dir = Path(save_file_path.as_posix()[
                                  :-len(save_file_path.suffix)])
        save_file_path_dir.mkdir(parents=True, exist_ok=True)
        save_file_path_dump = save_file_path_dir / f"{name}_{ix}.npz"
        if save_file_path_dump.exists():
            print(f"{name}_{ix} exists, skipping")
            continue

        bound[['y0', 'y1', 'x0', 'x1']] //= scale_division

        ar_slice = ar[bound['y0']:bound['y1'], bound['x0']:bound['x1']]
        ar_slice = glcm_pixel_normalize(ar_slice)
        g = glcm.run(ar_slice).astype(np.float16)
        crop = glcm.step_size + glcm.radius
        g = np.concatenate(
            [ar_slice[crop:-crop, crop:-crop, :, np.newaxis], g], axis=3)

        with open(save_file_path_dump, "wb") as f:
            pickle.dump(g, f)

        # Append to list if the key exists, else create
        if name in output.keys():
            output[name].append(g)
        else:
            output[name] = [g]

    return output


def glcm_pixel_normalize(ar: np.ndarray):
    return ar / ar.sum(axis=2)[..., np.newaxis]
