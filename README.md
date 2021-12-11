<p align="center">
    <img src="https://raw.githubusercontent.com/ad-astra-tech/wiser/main/resources/logo.png" />
</p>
<h2 align="center">wiser-gcloud-storage</h2>

[Wiser](https://github.com/ad-astra-tech/wiser) is a python package designed to free the developers from the burden of common operations with cloud technologies.
_Wiser_ gives you speed, effectiveness and allows you to truly focus on the application logic.

_Wiser_ comes with several straight-forward high-level interfaces that just work! You don't need to care about the 
underlying infrastructure layer, of the client connections or the data management: _Wiser_ will handle everything for you.

_wiser-gcloud-storage_ wraps Google Cloud Storage APIs. It depends on the core module [`wiser`](https://github.com/ad-astra-tech/wiser).

## Installation and usage

### Installation

_Wiser_ is published on [`PyPi`](https://pypi.org/project/wiser/). It requires Python 3.8+.

To install Google Cloud Firestore Wiser APIs run command `pip install 'wiser[gcloud-storage]'` or, alternatively, `pip install wiser-gcloud-storage`.

### Usage
_Wiser_ comes with several examples: you can find them in the [examples folder](https://github.com/nicolamassarenti/wiser/tree/main/package/examples/). A brief examples of the services currently supported is shown in the following.

GCP Storage supported types are: `.txt`, `.json`, `.npy`, `.jpg`, `.png` and `.pdf`. Below is shown some examples of the `get()` and `save()` APIs.

```python
import io
import os
import PyPDF2
import numpy as np
from PIL import Image
from wiser.gcloud.storage.services import Storage
from wiser.gcloud.storage.types.location import StorageLocationBuilder

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service-account.json"

# Text #################################################################################################################
location = (
    StorageLocationBuilder()
        .set_bucket(bucket="BUCKET_NAME")
        .set_blob_name(blob_name="path/to/sentence.txt")
        .build()
)
text = Storage.get(location=location)

# Numpy ################################################################################################################
location = (
    StorageLocationBuilder()
        .set_bucket(bucket=BUCKET_NAME)
        .set_blob_name(blob_name="path/to/array.npy")
        .build()
)
array = np.array(
    [[1, 2, 3], [1, 2, 3]]
)
Storage.save(obj=array, location=location)

# Image ################################################################################################################
image = Image.open("path/to/image.png")  # accepted also extension .jpg
location = (
    StorageLocationBuilder()
        .set_bucket(bucket=BUCKET_NAME)
        .set_blob_name(blob_name="folder_a/data.png")
        .build()
)

Storage.save(obj=image, location=location)
image = Image.open(
    io.BytesIO(
        Storage.get(location=location)
    )
)

# PDF ##################################################################################################################
pdf_path = "/path/to/file.pdf"
location = (
    StorageLocationBuilder()
    .set_bucket(bucket="BUCKET_NAME")
    .set_blob_name(blob_name="folder_a/data.pdf")
    .build()
)
Storage.save(obj=pdf_path, location=location)
pdf = PyPDF2.PdfFileReader(io.BytesIO(Storage.get(location=location)))
```

## Contributions and development

### Contributions
Contributors are welcome! You can either open an issue for a feature request or contact the owner to join the development.

### Development
Development guidelines are:

* **Straightforward APIs**: each module must be designed so to have easy-to-use APIS
* **Default first**: this package targets common operations, so it's ok to do not support fancy configurations
* **Black**: the code is indented with [`black`](https://github.com/psf/black)

    
## Testing
The adopted testing framework is [`unittest`](https://docs.python.org/3/library/unittest.html). To evaluate tests coverage is 
used [`coverage`](https://coverage.readthedocs.io/en/6.1.2/). 

To run unit tests execute:
```shell
coverage run -m --source wiser/  unittest discover -v
```
And to read the coverage report:
```shell
coverage report -m
```
## License

MIT