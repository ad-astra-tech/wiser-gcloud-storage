import os

from wiser.gcloud.services.storage import Storage
from wiser.gcloud.types.storage.location import StorageLocationBuilder

BUCKET_NAME = os.getenv("BUCKET_NAME")
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="path/to/service-account.json"

# Listing content of a bucket
location = StorageLocationBuilder().set_bucket(bucket=BUCKET_NAME).build()
blobs = Storage.get_list_content(location=location)
for blob in blobs:
    print(blob.complete_path())

# Listing content of a specific folder
location = (
    StorageLocationBuilder()
    .set_bucket(bucket=BUCKET_NAME)
    .set_blob_name(blob_name="folder_a")
    .build()
)
blobs = Storage.get_list_content(location=location)
for blob in blobs:
    print(blob.complete_path())
