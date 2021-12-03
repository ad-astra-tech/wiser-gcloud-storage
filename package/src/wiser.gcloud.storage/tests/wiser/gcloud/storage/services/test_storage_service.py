import unittest
from unittest.mock import patch

BUCKET = "bucket"
BLOB_NAME = "path/to/blob"


class StorageServiceTest(unittest.TestCase):
    def test_get_with_location_no_blob_name_raises_value_error(self):
        """
        GIVEN   a location with no blob_name (i.e. a folder)
        WHEN    if invoked `get()` method
        THEN    value error is raised
        """
        from wiser.gcloud.services.storage import Storage
        from wiser.gcloud.types.storage.location import StorageLocationBuilder

        location = StorageLocationBuilder().set_bucket(bucket=BUCKET).build()

        with self.assertRaises(ValueError):
            Storage.get(location=location)

    @patch("wiser.gcloud.connectors.storage.StorageConnector.download_as_string")
    def test_get_string(self, storage_connector_mock):
        """
        GIVEN   a valid location
        WHEN    the blob refers to a string
        THEN    the expected string is returned
        """
        from wiser.gcloud.services.storage import Storage
        from wiser.gcloud.types.storage.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/text.txt")
            .build()
        )

        data = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
        storage_connector_mock.return_value = data

        self.assertEqual(Storage.get(location=location), data)

    @patch("wiser.gcloud.connectors.storage.StorageConnector.download_as_string")
    def test_get_json(self, storage_connector_mock):
        """
        GIVEN   a valid location
        WHEN    the blob refers to a json file
        THEN    the expected json is returned
        """
        import json
        from wiser.gcloud.services.storage import Storage
        from wiser.gcloud.types.storage.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.json")
            .build()
        )

        data = {"1": "a", "2": "b"}
        storage_connector_mock.return_value = json.dumps(
            obj=data, sort_keys=True, indent=4, ensure_ascii=False
        )

        self.assertEqual(Storage.get(location=location), data)
