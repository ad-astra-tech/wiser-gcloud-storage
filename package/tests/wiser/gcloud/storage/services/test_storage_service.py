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
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = StorageLocationBuilder().set_bucket(bucket=BUCKET).build()

        with self.assertRaises(ValueError):
            Storage.get(location=location)

    @patch("wiser.gcloud.storage.connectors.StorageConnector.download_as_string")
    def test_get_string(self, storage_connector_mock):
        """
        GIVEN   a valid location
        WHEN    the blob refers to a string
        THEN    the expected string is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/text.txt")
            .build()
        )

        data = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
        storage_connector_mock.return_value = data

        self.assertEqual(Storage.get(location=location), data)

    @patch("wiser.gcloud.storage.connectors.StorageConnector.download_as_string")
    def test_get_json(self, storage_connector_mock):
        """
        GIVEN   a valid location
        WHEN    the blob refers to a json file
        THEN    the expected json is returned
        """
        import json
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

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

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.download_to_filename"
    )
    def test_get_numpy(self, storage_mock):
        """
        GIVEN   a valid location pointing to a numpy array data
        WHEN    Storage.get() is invoked
        THEN    the expected data is returned
        """
        import numpy as np
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.npy")
            .build()
        )

        data = np.array([1, 2, 3])

        def write_to_file(filename, bucket_name, source_blob_name):
            with open(filename, "wb") as f:
                np.save(f, data)

        storage_mock.side_effect = write_to_file

        self.assertEqual(data.tolist(), Storage.get(location=location).tolist())

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.download_as_bytes"
    )
    def test_get_jpg_png(self, storage_mock):
        """
        GIVEN   a valid location pointing to a jpg/png image
        WHEN    Storage.get() is invoked
        THEN    the expected data is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder
        import PIL.Image as Image
        import io

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.jpg")
            .build()
        )

        jpg_path = "./tests/stubs/data.jpg"
        img = Image.open(jpg_path)
        bytes_array = io.BytesIO()
        img.save(bytes_array, "jpeg")

        storage_mock.return_value = bytes_array

        self.assertEqual(bytes_array, Storage.get(location=location))

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.png")
            .build()
        )

        jpg_path = "./tests/stubs/data.png"
        img = Image.open(jpg_path)
        bytes_array = io.BytesIO()
        img.save(bytes_array, "png")

        storage_mock.return_value = bytes_array

        self.assertEqual(bytes_array, Storage.get(location=location))

    def test_get_jpg_png(self):
        """
        GIVEN   a valid location pointing to an unknown extension
        WHEN    Storage.get() is invoked
        THEN    Value Error is raised
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.xxpp")
            .build()
        )

        with self.assertRaises(ValueError):
            Storage.get(location=location)

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.download_as_bytes"
    )
    def test_get_pdf(self, storage_mock):
        """
        GIVEN   a valid location pointing to a PDF file
        WHEN    Storage.get() is invoked
        THEN    the content as bytes is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.pdf")
            .build()
        )

        pdf_path = "./tests/stubs/data.pdf"
        in_file = open(pdf_path, "rb")
        data = in_file.read()
        in_file.close()

        storage_mock.return_value = data

        self.assertEqual(data, Storage.get(location=location))

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.upload_from_file"
    )
    def test_save_numpy_returns_none(self, storage_mock):
        """
        GIVEN   a valid location pointing to a numpy object
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        import numpy as np
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.npy")
            .build()
        )

        data = np.array([1, 2, 3])

        storage_mock.return_value = None

        self.assertEqual(Storage.save(obj=data, location=location), None)

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.upload_from_file"
    )
    def test_save_png_jpg_returns_none(self, storage_mock):
        """
        GIVEN   a valid location pointing to a numpy object
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        from PIL import Image
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.png")
            .build()
        )
        png_path = "./tests/stubs/data.png"
        data = Image.open(png_path)
        storage_mock.return_value = None
        self.assertEqual(Storage.save(obj=data, location=location), None)
        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.png")
            .build()
        )

        jpg_path = "./tests/stubs/data.jpg"
        data = Image.open(jpg_path)
        storage_mock.return_value = None
        self.assertEqual(Storage.save(obj=data, location=location), None)

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.upload_from_string"
    )
    def test_save_txt_returns_none(self, storage_mock):
        """
        GIVEN   a valid location pointing to a txt fuke
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.txt")
            .build()
        )
        data = "Mock sentence"
        storage_mock.return_value = None
        self.assertEqual(Storage.save(obj=data, location=location), None)

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.upload_from_string"
    )
    def test_save_json_returns_none(self, storage_mock):
        """
        GIVEN   a valid location pointing to a json file
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.json")
            .build()
        )
        data = {"key_1": "value_1", "key_2": "value_2"}
        storage_mock.return_value = None
        self.assertEqual(Storage.save(obj=data, location=location), None)

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.upload_from_file"
    )
    def test_save_pdf_returns_none(self, storage_mock):
        """
        GIVEN   a valid location pointing to a pdf file
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.pdf")
            .build()
        )
        pdf_path = "./tests/stubs/data.pdf"
        storage_mock.return_value = None
        self.assertEqual(Storage.save(obj=pdf_path, location=location), None)

    @patch(
        "wiser.gcloud.storage.connectors.storage_connector.StorageConnector.upload_from_string"
    )
    def test_save_json_returns_none(self, storage_mock):
        """
        GIVEN   a valid location pointing to a json file
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.json")
            .build()
        )
        data = {"key_1": "value_1", "key_2": "value_2"}
        storage_mock.return_value = None
        self.assertEqual(Storage.save(obj=data, location=location), None)

    def test_save_unknown_format_raises_value_error(self):
        """
        GIVEN   a valid location pointing to an unknown format
        WHEN    Storage.save() is invoked
        THEN    None is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.xxks")
            .build()
        )
        data = "zaaaaa"
        with self.assertRaises(ValueError):
            Storage.save(obj=data, location=location)

    @patch("wiser.gcloud.storage.connectors.storage_connector.StorageConnector.exists")
    def test_exists_returns_true_if_exists(self, storage_mock):
        """
        GIVEN   a valid location pointing to an existing file
        WHEN    Storage.exists() is invoked
        THEN    True is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.json")
            .build()
        )
        storage_mock.return_value = True
        self.assertEqual(Storage.exists(location=location), True)

    @patch("wiser.gcloud.storage.connectors.storage_connector.StorageConnector.exists")
    def test_exists_returns_false_if_not_exist(self, storage_mock):
        """
        GIVEN   a valid location pointing to a not existing file
        WHEN    Storage.exists() is invoked
        THEN    False is returned
        """
        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/data.json")
            .build()
        )
        storage_mock.return_value = False
        self.assertEqual(Storage.exists(location=location), False)

    @patch("wiser.gcloud.storage.connectors.storage_connector.StorageConnector.copy")
    @patch("wiser.gcloud.storage.connectors.storage_connector.StorageConnector.delete")
    def test_move_returns_none(self, delete_mock, copy_mock):
        """
        GIVEN   two valid locations
        WHEN    Storage.move() is invoked
        THEN    None is returned
        """

        from wiser.gcloud.storage.services import Storage
        from wiser.gcloud.storage.types.location import StorageLocationBuilder

        location_1 = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/a/file.json")
            .build()
        )
        location_2 = (
            StorageLocationBuilder()
            .set_bucket(bucket=BUCKET)
            .set_blob_name(blob_name="path/to/b/file.json")
            .build()
        )

        delete_mock.return_value = None
        copy_mock.return_value = None

        self.assertEqual(
            Storage.move(source_location=location_1, dest_location=location_2), None
        )
