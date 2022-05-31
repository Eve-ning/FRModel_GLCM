from pathlib import Path
from tqdm import tqdm

from conf import PROJ_DIR
from create_report import Report
from upload import GCS
import os
os.chdir(PROJ_DIR.as_posix())

gcs = GCS()
for set_path, tree_paths in gcs.remote_set_paths().items():

    if any([t.name == "stacked_hist.jpg" for t in tree_paths]):
        print(f"Skipping set {set_path}, stacked hist exist.")
        continue

    set_path.mkdir(parents=True, exist_ok=True)

    tree_paths = list(filter(lambda p: p.suffix == '.npz', tree_paths))

    for tree_path in (t := tqdm(tree_paths)):
        t.set_description(f"DL Tree {tree_path.stem}")
        tree_path: Path
        if not tree_path.exists():
            gcs.download(tree_path)

    Report(set_path).create_report()
    gcs.upload_dir(set_path, True)
