from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from conf import INPUT_DIR, BOUNDS_FILE, IMAGE_EXTENSIONS, OUTPUT_DIR
from glcm_cupy import *
from glcm_sliced import glcm_sliced
from image_spec_loader import ImageSpecLoader


@dataclass
class FRModelGLCM:
    scale_division: int = 1
    glcm_in: GLCM = GLCM(bin_to=16, bin_from=1)
    save_file_ext: str = ".pickle"

    def run(self):
        """ Runs the script to convert images to GLCM """
        for bounds_path in self.get_bounds_paths():
            input_dir = bounds_path.parent
            if self.glcm_exists(input_dir):
                print(f"GLCM already exists for {input_dir}. Skipping")
                continue

            im_paths = self.get_im_paths(input_dir)
            im_spec = ImageSpecLoader.load(im_paths)
            glcm_sliced(
                self.glcm_in,
                ar=im_spec.ar_normalized,
                bounds_path=bounds_path,
                scale_division=self.scale_division,
                save_file_path=self.save_file_path(input_dir)
            )

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
               / (f"{self.glcm_in.radius}rad_{self.glcm_in.step_size}step_"
                  f"{self.glcm_in.bin_to}bins_{self.scale_division}xDownScale"
                  + self.save_file_ext)

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


FRModelGLCM(
    scale_division=3,
    glcm_in=GLCM(bin_to=2 ** 7, radius=4)
).run()
FRModelGLCM(
    scale_division=3,
    glcm_in=GLCM(bin_to=2 ** 7, radius=4, step_size=4)
).run()
# FRModelGLCM(bin_to=2**5, scale_division=5).run()
