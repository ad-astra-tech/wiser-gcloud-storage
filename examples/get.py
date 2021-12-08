import os
import io
from PIL import Image
import PyPDF2
from wiser.gcloud.storage.services import Storage
from wiser.gcloud.storage.types.location import StorageLocationBuilder

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

# PDF
pdf_path = "/path/to/file.pdf"
location = (
    StorageLocationBuilder()
    .set_bucket(bucket=BUCKET_NAME)
    .set_blob_name(blob_name="folder_a/data.pdf")
    .build()
)
Storage.save(obj=pdf_path, location=location)
pdf = PyPDF2.PdfFileReader(io.BytesIO(Storage.get(location=location)))
