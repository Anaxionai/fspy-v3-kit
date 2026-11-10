"""AzureBlobBackend: the StorageBackend interface on Azure Blob Storage, on Azurite (task 20).

azure-storage-blob is already in pyproject.toml. This is the module's AI move: a chat AI
translates S3Backend into this class, and your contract tests on Azurite decide whether to trust it.
"""

from __future__ import annotations  # see storage/base.py

from app.settings import BUCKET
from app.storage.base import UploadTarget


class AzureBlobBackend:
    """The same four methods on Azure Blob Storage, in the container reelpipe-uploads.

    Connect with the connection string in AZURE_STORAGE_CONNECTION_STRING.
    """

    def __init__(self, container: str = BUCKET) -> None:
        raise NotImplementedError("TODO(task 20): connect to the container with the connection string")

    def presign_upload(self, key: str, content_type: str, expires_s: int) -> UploadTarget:
        """A SAS URL for one blob, with create and write permission only, for expires_s seconds.

        headers must hold the Content-Type and "x-ms-blob-type": "BlockBlob".
        """
        raise NotImplementedError("TODO(task 20): make a SAS URL with create and write rights only")

    def get(self, key: str) -> bytes:
        """The blob's bytes. Raise KeyError if the blob does not exist."""
        raise NotImplementedError("TODO(task 20): download the blob, and turn a missing blob into KeyError")

    def put(self, key: str, data: bytes, content_type: str) -> None:
        """Save data as the blob key, replacing any blob that is already there."""
        raise NotImplementedError("TODO(task 20): upload the blob")

    def list(self, prefix: str) -> list[str]:
        """Every blob name that starts with prefix, or [] if there is none."""
        raise NotImplementedError("TODO(task 20): list the blob names under prefix")
