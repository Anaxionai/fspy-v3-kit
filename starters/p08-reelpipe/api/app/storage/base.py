"""The storage interface: one set of methods, and one adapter class per cloud (task 19).

The API, the worker and the tests call only these four methods, so they never know which
cloud they use. get_backend() in storage/__init__.py picks the adapter.
"""

# Lets `list[str]` below mean Python's list, although the class has a method called list.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class UploadTarget:
    """Where the browser uploads one file, and how.

    url: a presigned URL (S3), a SAS URL (Azure) or a signed URL (Google) that allows one PUT.
    headers: the headers the browser must send with that PUT, unchanged. Every cloud needs the
        Content-Type that was signed; Azure also needs "x-ms-blob-type": "BlockBlob".
    """

    url: str
    headers: dict[str, str] = field(default_factory=dict)


class StorageBackend(Protocol):
    """What every storage adapter can do. Keys look like uploads/<video_id>."""

    def presign_upload(self, key: str, content_type: str, expires_s: int) -> UploadTarget:
        """Return a URL that allows one PUT of key, with this content type, for expires_s seconds."""
        ...

    def get(self, key: str) -> bytes:
        """Return the object's bytes. Raise KeyError if there is no object with this key."""
        ...

    def put(self, key: str, data: bytes, content_type: str) -> None:
        """Save data at key, replacing any object that is already there."""
        ...

    def list(self, prefix: str) -> list[str]:
        """Return every key that starts with prefix, or [] if there is none."""
        ...
