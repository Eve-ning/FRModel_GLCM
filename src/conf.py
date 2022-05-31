from pathlib import Path

PROJ_DIR = Path(__file__).parent
DATA_DIR = PROJ_DIR / "data"
INPUT_DIR = DATA_DIR / "raw"
OUTPUT_DIR_GLCM = DATA_DIR / "glcm"
OUTPUT_DIR_GLCM_CROSS = DATA_DIR / "glcm_cross"

KEY_PATH = PROJ_DIR / "key/frmodel-4e6c3ce6ea28.json"
INFO_MD_FILE = DATA_DIR / "INFO.md"
INFO_CROSS_MD_FILE = DATA_DIR / "INFO_CROSS.md"
BOUNDS_FILE = "bounds.csv"