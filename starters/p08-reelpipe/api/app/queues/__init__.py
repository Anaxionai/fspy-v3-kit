"""The job queue behind one interface (task 19). Call get_queue() and use its four methods:

    from app.queues import get_queue
    get_queue().send(video_id, f"uploads/{video_id}")
"""

from app.queues.base import Job, JobQueue

__all__ = ["Job", "JobQueue", "get_queue"]


def get_queue() -> JobQueue:
    """Return the queue adapter that the QUEUE_BACKEND environment variable names.

    "sqs" (the default) gives SqsQueue from queues/sqs.py.
    TODO(task 21): "pubsub" gives PubSubQueue from queues/pubsub.py.
    For any other name, raise an error that names QUEUE_BACKEND, so a typing mistake shows at once.
    """
    raise NotImplementedError("TODO(task 19): read QUEUE_BACKEND and return the matching adapter")
