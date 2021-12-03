import json

from tempfile import TemporaryFile, NamedTemporaryFile

import numpy as np

from wiser.gcloud.storage.connectors.storage_connector import StorageConnector
from wiser.gcloud.storage.types.storage_location import (
    StorageLocation,
    StorageLocationBuilder,
)
from wiser.core.types.extensions import FileExtension


class Storage:
    def __str__(self):
        return "Google Cloud Storage Handler"

    @staticmethod
    def get(location: StorageLocation = None):
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
            NotImplementedError("File extension not managed")
            return

    @staticmethod
    def save(obj, location: StorageLocation = None):
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
            NotImplementedError("File extension not managed")
            return

    @staticmethod
    def exists(location: StorageLocation = None):
        return StorageConnector.exists(
            bucket_name=location.bucket, source_blob_name=location.blob_name
        )

    @staticmethod
    def get_list_content(location: StorageLocation = None) -> [StorageLocation]:
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
        source_location: StorageLocation = None,
        dest_location: StorageLocation = None,
    ):
        StorageConnector.copy(
            source_bucket_name=source_location.bucket,
            source_blob_name=source_location.blob_name,
            dest_bucket_name=dest_location.bucket,
            dest_blob_name=dest_location.blob_name,
        )
        return StorageConnector.delete(
            bucket_name=source_location.bucket,
            blob_name=source_location.blob_name,
        )