"""ReelPipe's worker: it takes jobs from reelpipe-jobs and makes a thumbnail and a 480p copy.

Run it in Docker from reelpipe/ (task 10):
    docker compose up --build worker
worker/Dockerfile sets PYTHONPATH=/app/api, so `from app.status import write_status` works here.

The keys are the same on every run, so running a job twice gives the same result:
    uploads/<video_id>              the original video
    outputs/<video_id>/thumb.jpg    the thumbnail
    outputs/<video_id>/480p.mp4     the 480p copy
"""

from pathlib import Path


def make_thumbnail(source: Path, thumb: Path) -> None:
    """Save one frame from 1 second in, 320 pixels wide, as the JPEG file thumb.

    Run the thumbnail command from task 10, step 3 with
    subprocess.run(args, check=True, capture_output=True). If ffmpeg cannot read the file,
    subprocess.CalledProcessError reaches the caller: do not catch it here.
    """
    raise NotImplementedError("TODO(task 10): run ffmpeg to make the thumbnail")


def make_480p(source: Path, copy: Path) -> None:
    """Write an H.264 MP4 whose short side is 480 pixels, as the file copy.

    Run your -crf 28 command from task 5, with -y and -movflags +faststart added (task 10, step 4).
    Use subprocess.run(args, check=True, capture_output=True), as for the thumbnail.
    """
    raise NotImplementedError("TODO(task 10): run ffmpeg to make the 480p copy")


def process_job(video_id: str, key: str) -> None:
    """Do one job from start to end. Raise if any step fails.

    Write status "processing", download key into a tempfile.TemporaryDirectory(), make the
    thumbnail and the 480p copy, upload both to outputs/<video_id>/, then write status "ready"
    with both output keys.

    TODO(task 12): if the status is already "ready", return at once. The job is idempotent:
        safe to run twice.
    TODO(task 19): download and upload through get_backend(), not boto3.
    """
    raise NotImplementedError("TODO(task 10): process one video")


def backoff_seconds(attempt: int) -> int:
    """How long a failed job waits before its next try, in seconds.

    attempt 1 waits 10, attempt 2 waits 20, attempt 3 waits 40: the wait doubles each time,
    and it is never more than 300.
    """
    raise NotImplementedError("TODO(task 12): return the back-off for this attempt")


def main() -> None:
    """Loop forever: take one job, process it, and delete its message only after the work is saved.

    Receive from reelpipe-jobs with WaitTimeSeconds=20 and MaxNumberOfMessages=1. Read video_id
    and key from the JSON body, call process_job(), and delete the message only after it returns.
    If ffmpeg fails (CalledProcessError), write status "failed" with the last line of its stderr,
    delete the message and keep looping.

    TODO(task 12): the attempt is the message's ApproximateReceiveCount; read MAX_ATTEMPTS
        (default 3) from the environment. Before the last attempt, do not delete: hide the message
        for backoff_seconds(attempt). On the last attempt, write "failed" and set its visibility
        to 0, so SQS moves it to reelpipe-jobs-dlq.
    TODO(task 19): take, delete and retry jobs through get_queue(), not boto3.
    """
    raise NotImplementedError("TODO(task 10): write the worker loop")


if __name__ == "__main__":
    main()
