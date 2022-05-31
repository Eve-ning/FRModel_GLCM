import json
import numpy as np
from dataclasses import dataclass, field
from google.cloud import storage
from google.cloud.storage import Blob, Bucket
from google.oauth2.service_account import Credentials
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict

from conf import OUTPUT_DIR_GLCM, OUTPUT_DIR_GLCM_CROSS, KEY_PATH, DATA_DIR


@dataclass
class GCS:
    bucket: Bucket = field(init=False, default=None)

    def __post_init__(self):
        with open(KEY_PATH) as f:
            j = json.load(f)
        credentials = Credentials.from_service_account_info(j)
        client = storage.Client(credentials=credentials, project='frmodel')
        self.bucket = client.get_bucket('tree-scan-data')

    def exists_on_cloud(self, local_path: Path):
        """ Whether the local file exists on the cloud """
        return self.bucket.blob(
            local_path.relative_to(DATA_DIR).as_posix()
        ).exists()

    def upload(self, local_path: Path, delete_on_upload: bool = True):
        """ Uploads current file to the remote """
        remote_path = local_path.relative_to(DATA_DIR)

        if not self.exists_on_cloud(local_path):
            self.bucket.blob(remote_path.as_posix()) \
                .upload_from_filename(local_path.as_posix())
        if delete_on_upload: local_path.unlink()

    def download(self, remote_path: Path):
        """ Uploads current file to the remote """
        if not self.exists_on_cloud(remote_path):
            print(f"File doesn't exist {remote_path}")
        else:
            self.bucket.blob(remote_path.as_posix()) \
                .download_to_filename(remote_path.as_posix())

    def upload_dir(self,
                   local_dir: Path = OUTPUT_DIR_GLCM,
                   delete_on_upload: bool = True):
        """ Uploads current directory to the remote """
        for ext in ("jpg", "md", "npz"):
            t = tqdm(list(local_dir.glob(f"**/*.{ext}")))
            for fn in t:
                t.set_description(f"Uploading {fn.stem}")
                self.upload(Path(fn), delete_on_upload)

    def remote_set_paths(
        self,
        extensions: List[str] = ('.npz', '.jpg')
    ) -> Dict[Path, List[Path]]:
        """ Get the tree set paths on the remote
        Parameters
        ----------
        extensions
            List of extensions to include for returned List of trees

        Returns
        -------
            A Dictionary of Key: Set Path, Value: List of Tree NPZ Paths
        """
        blobs: List[Blob] = list(
            filter(lambda b: b.name.endswith(".npz"),
                   self.bucket.list_blobs(prefix="glcm/")
                   )
        )

        sets = {}
        set_paths = np.unique(
            [Path(blob.name).parent for blob in blobs]).tolist()
        # noinspection PyTypeChecker
        for set_path in set_paths:
            tree_path: List[Path] = list(
                map(lambda b: Path(b.name),
                    filter(lambda b: b.name.endswith(extensions),
                           self.bucket.list_blobs(prefix=set_path.as_posix()))
                    )
            )
            sets[set_path] = tree_path

        return sets


def upload_glcm():
    GCS().upload_dir(OUTPUT_DIR_GLCM)


def upload_glcm_cross():
    GCS().upload_dir(OUTPUT_DIR_GLCM_CROSS)


