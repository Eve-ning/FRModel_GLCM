import json
import numpy as np
from google.cloud import storage
from google.cloud.storage import Blob
from google.oauth2.service_account import Credentials
from pathlib import Path
from tqdm import tqdm
from typing import List

from conf import KEY_PATH, PROJ_DIR
from create_report.create_group_report import Report
from upload.upload import upload_files

with open(KEY_PATH) as f:
    j = json.load(f)
credentials = Credentials.from_service_account_info(j)
client = storage.Client(credentials=credentials, project='frmodel')
bucket = client.get_bucket('tree-scan-data')
blobs = list(bucket.list_blobs(prefix="glcm/"))
blobs: List[Blob]
set_paths: List[Path] = \
    np.unique([Path(blob.name).parent for blob in blobs]).tolist()

for set_path in set_paths[:2]:
    tree_blobs: List[Blob] = list(bucket.list_blobs(prefix=set_path.as_posix()))
    if len([b for b in tree_blobs if b.name.endswith("stacked_hist.jpg")]) > 0:
        print(f"Skipping set {set_path}, stacked hist exist.")
        continue
    tree_blobs = [b for b in tree_blobs if b.name.endswith(".npz")]
    set_path.mkdir(parents=True, exist_ok=True)
    for blob in tqdm(tree_blobs, desc="Downloading NPZ"):
        dl_tgt = PROJ_DIR / set_path / Path(blob.name).name
        if not dl_tgt.exists():
            blob.download_to_filename(dl_tgt.as_posix())

    Report(PROJ_DIR / set_path).create_report()
    upload_files()
