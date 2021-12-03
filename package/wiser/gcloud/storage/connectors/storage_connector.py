from typing import List

from google.cloud import storage
from typing import TextIO, BinaryIO, Union


class StorageConnector:
    @staticmethod
    def upload_from_string(
        data: Union[bytes, str], bucket_name: str, destination_blob_name: str
    ) -> None:
        """
        Uploads data to the specified bucket with the specified blob name

        @param data: data to upload in bytes
        @param bucket_name: the destination bucket name
        @param destination_blob_name: the destination blob name
        @return: None
        """

        storage.Client().bucket(bucket_name=bucket_name).blob(
            blob_name=destination_blob_name
        ).upload_from_string(data=data)

    @staticmethod
    def upload_from_file(
        file_handle: Union[TextIO, BinaryIO],
        bucket_name: str,
        destination_blob_name: str,
    ) -> None:
        """
        Uploads data from filename

        @param source_file_name: the source filename
        @param bucket_name: the destination bucket name
        @param destination_blob_name: the destination blob name
        @return: None
        """
        storage.Client().bucket(bucket_name=bucket_name).blob(
            blob_name=destination_blob_name
        ).upload_from_file(file_handle)

    @staticmethod
    def download_as_bytes(bucket_name: str, source_blob_name: str) -> bytes:
        """
        Returns the content of a blob as bytes

        @param bucket_name: the source bucket name
        @param source_blob_name: the source blob name
        @return: the content of the blob as bytes
        """

        return (
            storage.Client()
            .bucket(bucket_name=bucket_name)
            .blob(blob_name=source_blob_name)
            .download_as_bytes()
        )

    @staticmethod
    def download_as_string(bucket_name: str, source_blob_name: str) -> str:
        """
        Returns the content of a blob as a string

        @param bucket_name: the source bucket name
        @param source_blob_name: the source blob name
        @return: the content of the blob as a string
        """

        return StorageConnector.download_as_bytes(
            bucket_name=bucket_name, source_blob_name=source_blob_name
        ).decode("utf-8")

    @staticmethod
    def download_to_filename(
        filename: str, bucket_name: str, source_blob_name: str
    ) -> None:
        """
        Returns the content of a blob to a filename

        @param filename: the name of the file
        @param bucket_name: the source bucket name
        @param source_blob_name: the source blob name
        @return: the content of the blob as a string
        """

        (
            storage.Client()
            .bucket(bucket_name=bucket_name)
            .blob(blob_name=source_blob_name)
            .download_to_filename(filename=filename)
        )

    @staticmethod
    def exists(bucket_name: str, source_blob_name: str) -> bool:
        """
        Returns True if the blob exists

        @param bucket_name: the source bucket name
        @param source_blob_name: the source blob name
        @return: True if gs://bucket_name/source_blob_name exists
        """

        return (
            storage.Client()
            .bucket(bucket_name=bucket_name)
            .blob(blob_name=source_blob_name)
            .exists()
        )

    @staticmethod
    def list_blobs(
        bucket_name: str, prefix: str = None, delimiter: str = None
    ) -> List[str]:
        """
        Returns the list of the blob names

        @param bucket_name: the source bucket name
        @param prefix: prefix to filter blobs
        @param delimiter: Delimiter, used with ``prefix`` to emulate hierarchy.
        @return: list of blob names that match the arguments
        """

        client = storage.Client()
        blobs = storage.Bucket(client=client, name=bucket_name).list_blobs(
            prefix=prefix, delimiter=delimiter
        )

        blobs_names = []
        for blob in blobs:
            blobs_names.append(blob.name)

        return blobs_names

    @staticmethod
    def copy(
        source_bucket_name: str,
        source_blob_name: str,
        dest_bucket_name: str,
        dest_blob_name: str,
    ) -> None:
        """
        Copies a blob to another location

        @param source_bucket_name: the source bucket name
        @param source_blob_name:  the source blob name
        @param dest_bucket_name: the destination bucket name
        @param dest_blob_name: the destination blob name
        @return: None
        """
        client = storage.Client()
        source_bucket = client.bucket(bucket_name=source_bucket_name)
        source_blob = source_bucket.blob(blob_name=source_blob_name)

        dest_bucket = client.bucket(bucket_name=dest_bucket_name)

        return source_bucket.copy_blob(
            blob=source_blob, destination_bucket=dest_bucket, new_name=dest_blob_name
        )

    @staticmethod
    def delete(bucket_name: str, blob_name: str) -> None:
        """
        Deletes a blob

        @param bucket_name: the source bucket name
        @param blob_name: the source blob name
        @return: None
        """
        return (
            storage.Client()
            .bucket(bucket_name=bucket_name)
            .blob(blob_name=blob_name)
            .delete()
        )
