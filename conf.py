import tifffile
from pathlib import Path

FILE_INFO = {
    "result.tif":
        dict(bits=8, channels=[0, 1, 2],
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
PROJ_DIR = Path(__file__).parent
INPUT_DIR = PROJ_DIR / "raw"
OUTPUT_DIR = PROJ_DIR / "glcm"
KEY_PATH = PROJ_DIR / "key/frmodel-4e6c3ce6ea28.json"
INFO_MD_FILE = PROJ_DIR / "INFO.md"
BOUNDS_FILE = "bounds.csv"

IMAGE_EXTENSIONS = ['tif', 'png', 'jpg']
CHANNELS = ["Wideband Red",
            "Wideband Green",
            "Wideband Blue",
            "RedEdge",
            "Blue",
            "NIR",
            "Red",
            "Green", ]
FEATURES = ["NONE",
            "HOMOGENEITY",
            "CONTRAST",
            "ASM",
            "MEAN",
            "VAR",
            "CORRELATION"]
NO_OF_FEATURES = 7
NO_OF_CHANNELS = 8
