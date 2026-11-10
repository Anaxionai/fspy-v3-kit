"""GcsBackend: the StorageBackend interface on Google Cloud Storage, on fake-gcs-server (task 21).

google-cloud-storage is already in pyproject.toml. The kit's cloudlab/gcp/README.md gives the
settings and makes the local signing key. Never copy that key file into reelpipe/.
"""

from __future__ import annotations  # see storage/base.py

from app.settings import BUCKET
from app.storage.base import UploadTarget


class GcsBackend:
    """The same four methods on Cloud Storage, in the bucket reelpipe-uploads.

    The client finds the emulator through STORAGE_EMULATOR_HOST.
    """

    def __init__(self, bucket: str = BUCKET) -> None:
        raise NotImplementedError("TODO(task 21): build the Cloud Storage client and keep the bucket")

    def presign_upload(self, key: str, content_type: str, expires_s: int) -> UploadTarget:
        """A V4 signed URL for one PUT of key, with this content type, for expires_s seconds.

        Sign it with the key file in GCS_SIGNING_KEY_FILE, and make it point at GCS_PUBLIC_URL,
        not at Google.
        headers must hold the Content-Type that was signed.
        """
        raise NotImplementedError("TODO(task 21): make a V4 signed PUT URL")

    def get(self, key: str) -> bytes:
        """The object's bytes. Raise KeyError if the object does not exist."""
        raise NotImplementedError("TODO(task 21): download the object, and turn NotFound into KeyError")

    def put(self, key: str, data: bytes, content_type: str) -> None:
        """Save data at key, replacing any object that is already there."""
        raise NotImplementedError("TODO(task 21): upload the object")

    def list(self, prefix: str) -> list[str]:
        """Every object name that starts with prefix, or [] if there is none."""
        raise NotImplementedError("TODO(task 21): list the object names under prefix")
