"""Send a job to the worker through the reelpipe-jobs queue (task 9).

A job is one JSON message: {"video_id": "<video_id>", "key": "uploads/<video_id>"}.
In task 19 the SQS call moves into queues/sqs.py, behind the JobQueue interface.
"""


def send_job(video_id: str, key: str) -> None:
    """Send one job for this video to reelpipe-jobs, as JSON.

    TODO(task 19): move the SQS call into SqsQueue.send in queues/sqs.py. Then call
        get_queue().send(video_id, key) here, or call it from main.py and delete this file.
    """
    raise NotImplementedError("TODO(task 9): send {'video_id': ..., 'key': ...} as JSON to reelpipe-jobs")
