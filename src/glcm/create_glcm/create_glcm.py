from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import List

from conf import INPUT_DIR, BOUNDS_FILE, OUTPUT_DIR_GLCM, \
    OUTPUT_DIR_GLCM_CROSS, INFO_MD_FILE, INFO_CROSS_MD_FILE, DATA_DIR
from glcm.create_glcm import glcm_sliced, ImageSpecLoader
from glcm.create_glcm.conf import IMAGE_EXTENSIONS
from glcm_cupy import GLCM, GLCMCross
from glcm_cupy.glcm_base import GLCMBase


@dataclass
class FRModelGLCM:
    scale_division: int = 1
    glcm_in: GLCMBase = field(
        default_factory=lambda: GLCM(bin_to=16, bin_from=1))
    minmax: bool = False
    pixel_norm: bool = False
    fn_append: str = ""
    output_dir: Path = OUTPUT_DIR_GLCM
    info_md_file_name: Path = INFO_MD_FILE

    def run(self):
        """ Runs the script to convert images to GLCM """

        for bounds_path in self.get_bounds_paths():
            input_dir = bounds_path.parent

            im_paths = self.get_im_paths(input_dir)
            im_spec = ImageSpecLoader.load(im_paths)
            glcm_sliced(
                self.glcm_in,
                ar=im_spec.ar_normalized,
                bounds_path=bounds_path,
                scale_division=self.scale_division,
                save_dir=self.save_dir(input_dir),
                minmax=self.minmax,
                pixel_norm=self.pixel_norm,
            )
            self.copy_info_md(self.save_dir(input_dir))

    def save_dir(self, input_dir: Path) -> Path:
        """ Get the Save File Dir Path

        Parameters
        ----------
        input_dir
            Path of the Input Directory
        """

        if isinstance(self.glcm_in, GLCM):

            return self.output_dir \
                   / Path(
                os.path.join(*input_dir.relative_to(DATA_DIR).parts[1:])) \
                   / (
                       f"{'minmax_' if self.minmax else ''}"
                       f"{'pixnorm_' if self.pixel_norm else ''}"
                       f"{self.glcm_in.radius}rad_"
                       f"{self.glcm_in.step_size}step_"
                       f"{self.glcm_in.bin_to}bins_"
                       f"{self.scale_division}xDownScale"
                   )
        else:

            return self.output_dir \
                   / Path(
                os.path.join(*input_dir.relative_to(DATA_DIR).parts[1:])) \
                   / (
                       f"{'minmax_' if self.minmax else ''}"
                       f"{'pixnorm_' if self.pixel_norm else ''}"
                       f"{self.glcm_in.radius}rad_"
                       f"{self.glcm_in.bin_to}bins_"
                       f"{self.scale_division}xDownScale"
                       f"{self.fn_append}"
                   )

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
        return self.save_dir(input_dir).exists()

    def copy_info_md(self, save_dir):
        shutil.copy(self.info_md_file_name, save_dir)


def create_glcm(bit: int,
                radius: int,
                step_size: int):
    FRModelGLCM(
        glcm_in=GLCM(
            bin_from=1,
            bin_to=2 ** bit,
            radius=radius,
            step_size=step_size
        ),
        output_dir=OUTPUT_DIR_GLCM,
        info_md_file_name=INFO_MD_FILE
    ).run()


def create_glcm_cross(bit: int,
                      radius: int):
    g = GLCMCross(
        bin_from=1,
        bin_to=2 ** bit,
        radius=radius,
    )
    FRModelGLCM(
        glcm_in=g,
        fn_append="_all_combos",
        output_dir=OUTPUT_DIR_GLCM_CROSS
    ).run()
