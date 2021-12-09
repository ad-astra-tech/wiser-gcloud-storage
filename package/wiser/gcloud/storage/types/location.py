from __future__ import annotations

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class StorageLocation(BaseModel):
    prefix: str = Field(
        default="gs://",
        description="Google Cloud Storage prefix",
        example="gs://",
        const=True,
    )
    bucket: str = Field(
        ...,
        description="Google Cloud Storage bucket",
        example="my-bucket",
        min_length=1,
        read_only=True,
    )
    blob_name: Optional[str] = Field(
        description="Google Cloud Storage blob path",
        example="path/to/something.ext",
        read_only=True,
    )
    folders: Optional[str] = Field(
        description="Google Cloud Storage folder path",
        example="path/to/",
        read_only=True,
    )
    filename: Optional[str] = Field(
        description="Google Cloud Storage blob extension",
        example="something.ext",
        read_only=True,
    )

    def complete_path(self):
        tail = ""
        if self.blob_name is not None:
            tail = str(self.blob_name)
        return str(self.prefix) + str(self.bucket) + "/" + tail


class StorageLocationBuilder(BaseModel):
    prefix: str = Field(
        default="gs://", description="Google Cloud Storage prefix", example="gs://"
    )
    bucket: str = Field(
        default=None,
        description="Google Cloud Storage bucket",
        example="my-bucket",
        min_length=1,
    )
    blob_name: str = Field(
        default=None,
        description="Google Cloud Storage blob path",
        example="path/to/something.ext",
    )
    folders: str = Field(
        default=None, description="Google Cloud Storage folder path", example="path/to/"
    )
    filename: str = Field(
        default=None,
        description="Google Cloud Storage blob extension",
        example="something.ext",
    )

    def set_prefix(self, prefix: str) -> StorageLocationBuilder:
        self.prefix = prefix
        return self

    def set_bucket(self, bucket: str) -> StorageLocationBuilder:
        self.bucket = bucket
        return self

    def set_blob_name(self, blob_name: str) -> StorageLocationBuilder:
        self.blob_name = blob_name
        return self

    def build(self) -> StorageLocation:
        # Getting filename from blob_name
        if self.blob_name is not None:
            self.folders = self.blob_name
            if "." in Path(self.blob_name).name:
                values = self.blob_name.split("/")
                self.filename = values[-1]
                self.folders = "/".join(values[:-1])

        return StorageLocation(
            bucket=self.bucket,
            folders=self.folders,
            blob_name=self.blob_name,
            filename=self.filename,
        )
