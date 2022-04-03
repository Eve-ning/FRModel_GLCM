from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List

from glcm_cupy import *

from conf import INPUT_DIR, BOUNDS_FILE, IMAGE_EXTENSIONS, OUTPUT_DIR
from glcm_sliced import glcm_sliced
from image_spec_loader import ImageSpecLoader


@dataclass
class FRModelGLCM:
    bin_to: int = 4
    scale_division: int = 5

    save_file_name: str = "result.pickle"

    def run(self):
        """ Runs the script to convert images to GLCM

        Returns
        -------

        """
        for bounds_path in self.get_bounds_paths():
            input_dir = bounds_path.parent
            if self.glcm_exists(input_dir):
                print(f"GLCM already exists for {input_dir}. Skipping")
                continue

            im_paths = self.get_im_paths(input_dir)

            im_spec = ImageSpecLoader.load(im_paths)

            slices = glcm_sliced(
                GLCM(bin_to=self.bin_to),
                ar=im_spec.ar_normalized,
                bounds_path=bounds_path,
                scale_division=self.scale_division
            )
            self.save(slices, input_dir)

    def save(self, obj: object, input_dir: Path) -> None:
        """ Saves the object, relative to the input dir's pathing

        Parameters
        ----------
        obj
            Object to pickle and save
        input_dir
            The Pathing of the input images

        """
        save_file = self.save_file_path(input_dir)
        save_file.parent.mkdir(parents=True, exist_ok=True)
        with open(save_file, "wb") as f:
            pickle.dump(obj, f)

    def save_file_path(self, input_dir: Path) -> Path:
        """ Get the Save File Path

        Parameters
        ----------
        input_dir
            Path of the Input Directory

        Returns
        -------
        Path
            Path of the output file

        """
        return OUTPUT_DIR \
               / Path(os.path.join(*input_dir.parts[1:])) \
               / self.save_file_name

    @staticmethod
    def get_bounds_paths() -> List[Path]:
        """ Gets the File Path of the bounds

        Returns
        -------

        """
        paths = []
        for path in list(INPUT_DIR.glob("**/*")):
            if path.name == BOUNDS_FILE:
                paths.append(path)
        return paths

    @staticmethod
    def get_im_paths(input_dir: Path) -> List[Path]:
        """ Gets all paths of the images

        Parameters
        ----------
        input_dir
            Directory of the images

        Returns
        -------
        List[Path]
            List of all image paths
        """
        return [_
                for ext in IMAGE_EXTENSIONS
                for _ in input_dir.glob(f"*.{ext}")]

    def glcm_exists(self, input_dir: Path) -> bool:
        """ Checks if the GLCM exists already

        Parameters
        ----------
        input_dir
            Directory of Images

        Returns
        -------
        bool
            If GLCM exists
        """
        return self.save_file_path(input_dir).exists()


# %%
FRModelGLCM().run()

# %%
FRModelGLCM.get_bounds_paths()
# %%
with open("outputs/18Dec2020/result.pickle", "rb") as f:
    out = pickle.load(f)
