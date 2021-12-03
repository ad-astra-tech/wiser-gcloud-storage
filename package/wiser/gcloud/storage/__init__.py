try:
    import pkg_resources

    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil

    __path__ = pkgutil.extend_path(__path__, __name__)

from wiser.gcloud.storage.services import Storage
from wiser.gcloud.storage.connectors import StorageConnector
from wiser.gcloud.storage.types import StorageLocationBuilder, StorageLocation

__all__ = ["Storage", "StorageLocationBuilder", "StorageLocation", "StorageConnector"]
