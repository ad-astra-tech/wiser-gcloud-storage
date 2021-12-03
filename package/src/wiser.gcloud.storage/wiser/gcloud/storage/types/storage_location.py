from __future__ import annotations

from pathlib import Path


class StorageLocation:
    def __init__(
        self, prefix: str, bucket: str, blob_name: str, folders: str, filename: str
    ):
        self._prefix = prefix
        self._bucket = bucket
        self._blob_name = blob_name
        self._folders = folders
        self._filename = filename

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def folders(self) -> str:
        return self._folders

    @property
    def blob_name(self) -> str:
        return self._blob_name

    @property
    def bucket(self) -> str:
        return self._bucket

    @property
    def prefix(self) -> str:
        return self._prefix

    def complete_path(self):
        tail = ""
        if self._blob_name is not None:
            tail = str(self.blob_name)
        return str(self.prefix) + str(self.bucket) + "/" + tail


class StorageLocationBuilder:
    def __init__(self):
        self._prefix = "gs://"
        self._bucket = None
        self._blob_name = None
        self._filename = None
        self._folders = None

    def set_prefix(self, prefix: str) -> StorageLocationBuilder:
        self._prefix = prefix
        return self

    def set_bucket(self, bucket: str) -> StorageLocationBuilder:
        self._bucket = bucket
        return self

    def set_blob_name(self, blob_name: str) -> StorageLocationBuilder:
        self._blob_name = blob_name
        return self

    def build(self) -> StorageLocation:
        # Validating setting
        if self._bucket is None:
            raise ValueError("Bucket not set")

        # Getting filename from blob_name
        if self._blob_name is not None:
            self._folders = self._blob_name
            if "." in Path(self._blob_name).name:
                values = self._blob_name.split("/")
                self._filename = values[-1]
                self._folders = "/".join(values[:-1])

        return StorageLocation(
            prefix=self._prefix,
            bucket=self._bucket,
            folders=self._folders,
            blob_name=self._blob_name,
            filename=self._filename,
        )
