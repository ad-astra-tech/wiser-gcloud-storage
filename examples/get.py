import os
import io
from PIL import Image
from wiser.gcloud.services.storage import Storage
from wiser.gcloud.types.storage.location import StorageLocationBuilder

BUCKET_NAME = os.getenv("BUCKET_NAME")
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="path/to/service-account.json"

# Text
location = (
    StorageLocationBuilder()
    .set_bucket(bucket=BUCKET_NAME)
    .set_blob_name(blob_name="folder_a/folder_b/sentence.txt")
    .build()
)
text = Storage.get(location=location)

# Numpy array
location = (
    StorageLocationBuilder()
    .set_bucket(bucket=BUCKET_NAME)
    .set_blob_name(blob_name="folder_a/data.npy")
    .build()
)
array = Storage.get(location=location)

# JSON
location = (
    StorageLocationBuilder()
    .set_bucket(bucket=BUCKET_NAME)
    .set_blob_name(blob_name="folder_a/folder_c/data.json")
    .build()
)

data = Storage.get(location=location)

# JPG, PNG
image_path = os.environ["IMAGE_PATH"]

location = (
    StorageLocationBuilder()
    .set_bucket(bucket=BUCKET_NAME)
    .set_blob_name(blob_name="folder_a/data.jpg")
    .build()
)

image = Image.open(io.BytesIO(Storage.get(location=location)))
