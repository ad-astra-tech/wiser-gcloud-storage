import json

from tempfile import TemporaryFile, NamedTemporaryFile
from typing import Any

import numpy as np

from wiser.gcloud.storage.connectors.storage_connector import StorageConnector
from wiser.gcloud.storage.types.location import (
    StorageLocation,
    StorageLocationBuilder,
)
from wiser.core.types.extensions import FileExtension


class Storage:
    @staticmethod
    def get(location: StorageLocation = None) -> Any:
        if location.blob_name is None:
            raise ValueError("No blob name given")

        if location.filename.endswith(FileExtension.NUMPY):
            tmp_file = NamedTemporaryFile()
            StorageConnector.download_to_filename(
                filename=tmp_file.name,
                bucket_name=location.bucket,
                source_blob_name=location.blob_name,
            )
            tmp_file.seek(0)
            data = np.load(tmp_file)
            tmp_file.close()
            return data

        elif location.filename.endswith(
            FileExtension.JPG
        ) or location.filename.endswith(FileExtension.PNG):
            return StorageConnector.download_as_bytes(
                bucket_name=location.bucket, source_blob_name=location.blob_name
            )

        elif location.filename.endswith(FileExtension.JSON):
            data = StorageConnector.download_as_string(
                bucket_name=location.bucket, source_blob_name=location.blob_name
            )
            return json.loads(data)
        elif location.filename.endswith(FileExtension.TEXT):
            data = StorageConnector.download_as_string(
                bucket_name=location.bucket, source_blob_name=location.blob_name
            )
            return data
        elif location.filename.endswith(FileExtension.PDF):
            data = StorageConnector.download_as_bytes(
                bucket_name=location.bucket, source_blob_name=location.blob_name
            )
            return data
        else:
            raise ValueError("File extension not managed")

    @staticmethod
    def save(obj, location: StorageLocation = None) -> None:
        if location.filename.endswith(FileExtension.NUMPY):
            tmp_file = TemporaryFile()
            np.save(tmp_file, obj)
            tmp_file.seek(0)
            StorageConnector.upload_from_file(
                tmp_file,
                bucket_name=location.bucket,
                destination_blob_name=location.blob_name,
            )
            tmp_file.close()

        elif location.filename.endswith(
            FileExtension.JPG
        ) or location.filename.endswith(FileExtension.PNG):
            tmp_file = NamedTemporaryFile()
            tmp_file.name = location.filename
            obj.save(tmp_file)
            tmp_file.seek(0)
            StorageConnector.upload_from_file(
                tmp_file,
                bucket_name=location.bucket,
                destination_blob_name=location.blob_name,
            )
            tmp_file.close()

        elif location.filename.endswith(FileExtension.TEXT):
            data = obj
            StorageConnector.upload_from_string(
                data=data,
                bucket_name=location.bucket,
                destination_blob_name=location.blob_name,
            )
        elif location.filename.endswith(FileExtension.JSON):
            data = json.dumps(obj=obj, sort_keys=True, indent=4, ensure_ascii=False)
            StorageConnector.upload_from_string(
                data=data,
                bucket_name=location.bucket,
                destination_blob_name=location.blob_name,
            )
        elif location.filename.endswith(FileExtension.PDF):
            with open(obj, "rb") as f:
                StorageConnector.upload_from_file(
                    file_handle=f,
                    bucket_name=location.bucket,
                    destination_blob_name=location.blob_name,
                )
        else:
            raise ValueError("File extension not managed")

    @staticmethod
    def exists(location: StorageLocation) -> bool:
        return StorageConnector.exists(
            bucket_name=location.bucket, source_blob_name=location.blob_name
        )

    @staticmethod
    def get_list_content(location: StorageLocation) -> [StorageLocation]:
        blobs = StorageConnector.list_blobs(
            bucket_name=location.bucket, prefix=location.folders
        )

        locations_list = []
        for blob_name in blobs:
            if blob_name == location.folders:
                # blob is the folder, not a file
                continue
            base_location = (
                StorageLocationBuilder()
                .set_bucket(bucket=location.bucket)
                .set_blob_name(blob_name=blob_name)
                .build()
            )
            locations_list.append(base_location)

        return locations_list

    @staticmethod
    def move(
        source_location: StorageLocation,
        dest_location: StorageLocation,
    ) -> None:
        StorageConnector.copy(
            source_bucket_name=source_location.bucket,
            source_blob_name=source_location.blob_name,
            dest_bucket_name=dest_location.bucket,
            dest_blob_name=dest_location.blob_name,
        )
        StorageConnector.delete(
            bucket_name=source_location.bucket,
            blob_name=source_location.blob_name,
        )
