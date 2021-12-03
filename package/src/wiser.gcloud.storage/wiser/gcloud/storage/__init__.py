try:
    import pkg_resources

    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil

    __path__ = pkgutil.extend_path(__path__, __name__)

from wiser.gcloud.storage.services.storage_service import Storage
from wiser.gcloud.storage.types.storage_location import StorageLocationBuilder

__all__ = ["Storage", "StorageLocationBuilder"]
