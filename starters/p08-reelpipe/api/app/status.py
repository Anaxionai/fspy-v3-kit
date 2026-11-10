"""Each video's status, kept as JSON in the bucket at status/<video_id>.json (task 9).

ReelPipe has no database. A status record is a small JSON object, for example:
    {"id": "<video_id>", "status": "processing", "updated_at": "2026-12-01T10:15:00+05:30"}
The API and the worker both use these functions, so every record has the same shape.
"""

STATUSES = ("uploaded", "processing", "ready", "failed")


def write_status(video_id: str, status: str, **fields) -> dict:
    """Save a video's status record at status/<video_id>.json and return the record.

    status is one of STATUSES. The record holds "id" and "status", plus every extra field you pass:
        write_status(video_id, "failed", error="Invalid data found when processing input")
    Store a time as well, such as updated_at, so GET /videos can sort the records newest first.

    TODO(task 19): save it with get_backend().put(...) instead of calling boto3 here.
    """
    raise NotImplementedError("TODO(task 9): save the record as JSON at status/<video_id>.json")


def read_status(video_id: str) -> dict | None:
    """Return a video's status record, or None if it has no record yet.

    TODO(task 19): read it with get_backend().get(...), which raises KeyError for a missing key.
    """
    raise NotImplementedError("TODO(task 9): read status/<video_id>.json, or return None")


def list_statuses() -> list[dict]:
    """Return every status record under status/, newest first. GET /videos uses it.

    TODO(task 19): list and read the records through get_backend().
    """
    raise NotImplementedError("TODO(task 9): read every record under status/, newest first")
