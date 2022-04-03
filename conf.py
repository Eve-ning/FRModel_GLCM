from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

FILE_INFO = {
    "result.tif":
        dict(bits=8, channels=[0,1,2],
             channel_names=["Wideband Red", "Wideband Green", "Wideband Blue"],
             read_method=tifffile.imread),
    "result_Red.tif":
        dict(bits=14, channels=None, channel_names=["Red"],
             read_method=tifffile.imread),
    "result_Green.tif":
        dict(bits=14, channels=None, channel_names=["Green"],
             read_method=tifffile.imread),
    "result_Blue.tif":
        dict(bits=14, channels=None, channel_names=["Blue"],
             read_method=tifffile.imread),
    "result_NIR.tif":
        dict(bits=14, channels=None, channel_names=["NIR"],
             read_method=tifffile.imread),
    "result_RedEdge.tif":
        dict(bits=14, channels=None, channel_names=["RedEdge"],
             read_method=tifffile.imread),
}
INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
BOUNDS_FILE = "bounds.csv"

IMAGE_EXTENSIONS = ['tif', 'png', 'jpg']