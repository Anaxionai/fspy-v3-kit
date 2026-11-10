"""Storage behind one interface (task 19). Call get_backend() and use its four methods:

    from app.storage import get_backend
    storage = get_backend()
    storage.put("status/abc.json", b"{}", "application/json")
"""

from app.storage.base import StorageBackend, UploadTarget

__all__ = ["StorageBackend", "UploadTarget", "get_backend"]


def get_backend() -> StorageBackend:
    """Return the storage adapter that the STORAGE_BACKEND environment variable names.

    "s3" (the default) gives S3Backend from storage/s3.py.
    TODO(task 20): "azure" gives AzureBlobBackend from storage/azure_blob.py.
    TODO(task 21): "gcs" gives GcsBackend from storage/gcs.py.
    For any other name, raise an error that names STORAGE_BACKEND, so a typing mistake shows at once.
    """
    raise NotImplementedError("TODO(task 19): read STORAGE_BACKEND and return the matching adapter")
