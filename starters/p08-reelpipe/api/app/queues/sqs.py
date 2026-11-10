"""SqsQueue: the JobQueue interface on Amazon SQS, which Floci emulates (task 19)."""

from __future__ import annotations

from app.queues.base import Job
from app.settings import QUEUE


class SqsQueue:
    """Every SQS call of the API and the worker moves in here: send_job's and the worker loop's."""

    def __init__(self, queue_name: str = QUEUE) -> None:
        raise NotImplementedError("TODO(task 19): build the SQS client and find the queue")

    def send(self, video_id: str, key: str) -> None:
        """Send the job as a JSON message."""
        raise NotImplementedError("TODO(task 19): move the SQS call of send_job here")

    def receive(self, wait_s: int = 20) -> Job | None:
        """Long-poll for at most one message and turn it into a Job, or return None."""
        raise NotImplementedError("TODO(task 19): move the worker's receive_message call here")

    def delete(self, job: Job) -> None:
        """Delete the message, after the work is saved."""
        raise NotImplementedError("TODO(task 19): move the worker's delete_message call here")

    def retry_later(self, job: Job, delay_s: int) -> None:
        """Hide the message for delay_s seconds, so it comes back later."""
        raise NotImplementedError("TODO(task 19): move the worker's change_message_visibility call here")
