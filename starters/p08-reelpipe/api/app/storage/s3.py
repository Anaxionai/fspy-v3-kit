"""S3Backend: the StorageBackend interface on Amazon S3, which Floci emulates (task 19)."""

from __future__ import annotations  # see storage/base.py

from app.settings import BUCKET
from app.storage.base import UploadTarget


class S3Backend:
    """Every S3 call of the API and the worker moves in here.

    Build the S3 client once, in __init__, the way you built it in task 8: endpoint_url from
    AWS_ENDPOINT_URL, signature version s3v4 and path-style addressing.
    """

    def __init__(self, bucket: str = BUCKET) -> None:
        raise NotImplementedError("TODO(task 19): keep the bucket name and build the S3 client")

    def presign_upload(self, key: str, content_type: str, expires_s: int) -> UploadTarget:
        """A presigned PUT URL for key with the content type signed, and the headers to send."""
        raise NotImplementedError("TODO(task 19): move your presigning code from POST /uploads here")

    def get(self, key: str) -> bytes:
        """The object's bytes. Raise KeyError if the key does not exist."""
        raise NotImplementedError("TODO(task 19): get the object, and turn a missing key into KeyError")

    def put(self, key: str, data: bytes, content_type: str) -> None:
        """Save data at key, replacing any object that is already there."""
        raise NotImplementedError("TODO(task 19): put the object")

    def list(self, prefix: str) -> list[str]:
        """Every key that starts with prefix, or [] if there is none."""
        raise NotImplementedError("TODO(task 19): list the keys under prefix")
