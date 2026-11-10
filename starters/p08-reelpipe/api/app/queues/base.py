"""The job-queue interface: one set of methods, and one adapter class per queue service (task 19).

The API sends jobs and the worker takes them, through these four methods only.
get_queue() in queues/__init__.py picks the adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Job:
    """One job the worker has taken from the queue.

    video_id, key: from the message body {"video_id": ..., "key": ...}.
    attempt: how many times this message has been delivered, counting from 1
        (ApproximateReceiveCount on SQS, delivery_attempt on Pub/Sub).
    handle: what delete() and retry_later() need to find the message again
        (the ReceiptHandle on SQS, the ack_id on Pub/Sub).
    """

    video_id: str
    key: str
    attempt: int
    handle: str


class JobQueue(Protocol):
    """What every queue adapter can do."""

    def send(self, video_id: str, key: str) -> None:
        """Put one job on the queue as JSON: {"video_id": video_id, "key": key}."""
        ...

    def receive(self, wait_s: int = 20) -> Job | None:
        """Wait up to wait_s seconds for one job. Return None if no job came."""
        ...

    def delete(self, job: Job) -> None:
        """Remove the job for good, after its work is saved (delete on SQS, acknowledge on Pub/Sub)."""
        ...

    def retry_later(self, job: Job, delay_s: int) -> None:
        """Make the job come back after delay_s seconds. 0 means at once."""
        ...
