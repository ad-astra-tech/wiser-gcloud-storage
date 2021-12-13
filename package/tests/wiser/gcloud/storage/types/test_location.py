import unittest


class StorageLocationTest(unittest.TestCase):
    def test_location_builder_no_bucket_raises_valueerror(self):
        """
        GIVEN StorageLocationBuilder
        WHEN  the bucket is not set
        THEN a value error is raised
        """

        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        with self.assertRaises(ValueError):
            StorageLocationBuilder().set_blob_name(
                blob_name="folder_a/folder_b/filename"
            ).build()

    def test_location_builder_no_blob_name_returns_a_valid_location(self):
        """
        GIVEN   LocationBuilder
        WHEN    no blob_name is injected
        THEN    a valid location is returned
        """

        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = StorageLocationBuilder().set_bucket(bucket="bucket").build()

        self.assertEqual(location.blob_name, None)
        self.assertEqual(location.folders, None)
        self.assertEqual(location.filename, None)
        self.assertEqual(location.bucket, "bucket")
        self.assertEqual(location.prefix, "gs://")
        self.assertEqual(location.complete_path(), "gs://bucket/")

    def test_location_builder_returns_storage_location(self):
        """
        GIVEN LocationBuilder
        WHEN  the blob name and the bucket are set
        THEN a fully featured storage location object is returned
        """

        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        prefix = "gs://"
        bucket = "bucket_name"
        filename = "filename.json"
        folders = "folder_a"
        blob_name = folders + "/" + filename
        complete_path = prefix + bucket + "/" + blob_name

        storage_location = (
            StorageLocationBuilder()
            .set_prefix(prefix="gs://")
            .set_bucket(bucket=bucket)
            .set_blob_name(blob_name="folder_a/filename.json")
            .build()
        )

        self.assertEqual(storage_location.prefix, prefix)
        self.assertEqual(storage_location.bucket, bucket)
        self.assertEqual(storage_location.folders, folders)
        self.assertEqual(storage_location.filename, filename)
        self.assertEqual(storage_location.blob_name, blob_name)
        self.assertEqual(storage_location.complete_path(), complete_path)

    def test_from_valid_uri_returns_valid_location(self):
        """
        GIVEN LocationBuilder and a valid uri
        WHEN  the 'from_uri()' is invoked
        THEN  a valid storage location is returned
        """

        from wiser.gcloud.storage.types.location import StorageLocationBuilder, StorageLocation

        bucket = "bucket"
        folders = "path/to"
        filename = "doc.pdf"
        blob_name = "{folders}/{filename}".format(folders=folders, filename=filename)
        uri = "gs://{bucket}/{blob_name}".format(bucket=bucket, blob_name=blob_name)

        location = StorageLocationBuilder().from_uri(uri=uri).build()

        self.assertIsInstance(location, StorageLocation)
        self.assertEqual(location.bucket, bucket)
        self.assertEqual(location.folders, folders)
        self.assertEqual(location.filename, filename)
        self.assertEqual(location.blob_name, blob_name)

    def test_from_invalid_uri_raises_value_error(self):
        """
        GIVEN LocationBuilder and an invalid uri
        WHEN  the 'from_uri()' is invoked
        THEN  value error is raised
        """

        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        with self.assertRaises(ValueError):
            StorageLocationBuilder().from_uri(uri="https://something/to/docs.csc").build()

        with self.assertRaises(ValueError):
            StorageLocationBuilder().from_uri(uri="gs:///path/to/docs.pdf").build()