"""PubSubQueue: the JobQueue interface on Google Pub/Sub, on the Pub/Sub emulator (task 21).

Jobs are published to the topic reelpipe-jobs and pulled from the subscription reelpipe-jobs-sub.
The clients find the emulator through PUBSUB_EMULATOR_HOST. The project id is in
GOOGLE_CLOUD_PROJECT (fspy-local in the kit's cloud lab).
"""

from __future__ import annotations

from app.queues.base import Job
from app.settings import QUEUE, SUBSCRIPTION


class PubSubQueue:
    """The same four methods on Pub/Sub. Set MAX_ATTEMPTS=5 for Pub/Sub runs (task 21)."""

    def __init__(self, topic: str = QUEUE, subscription: str = SUBSCRIPTION) -> None:
        raise NotImplementedError("TODO(task 21): build the publisher and the subscriber clients")

    def send(self, video_id: str, key: str) -> None:
        """Publish the job as JSON to the topic."""
        raise NotImplementedError("TODO(task 21): publish the job")

    def receive(self, wait_s: int = 20) -> Job | None:
        """Pull at most one message and turn it into a Job, or return None.

        Job.attempt comes from the message's delivery_attempt, and Job.handle is its ack_id.
        """
        raise NotImplementedError("TODO(task 21): pull one message")

    def delete(self, job: Job) -> None:
        """Acknowledge the message, after the work is saved."""
        raise NotImplementedError("TODO(task 21): acknowledge the message")

    def retry_later(self, job: Job, delay_s: int) -> None:
        """Give the message a new ack deadline of delay_s seconds, so it comes back later."""
        raise NotImplementedError("TODO(task 21): change the ack deadline with modify_ack_deadline")
