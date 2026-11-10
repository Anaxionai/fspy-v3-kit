"""ReelPipe's Lambda function: an S3 event becomes a status record and one job (task 18).

Deploy it with `bash lambda/deploy.sh`. It is zipped on its own as function.zip, so it cannot
import app/ from api/: it calls boto3 directly, and the Lambda runtime already has boto3.
Floci gives the function AWS_ENDPOINT_URL, so plain boto3 clients reach Floci.
"""

BUCKET = "reelpipe-uploads"
QUEUE = "reelpipe-jobs"

# TODO(task 18): create the S3 and SQS clients here, outside handler(), so a warm start reuses them.


def video_ids(event: dict) -> list[str]:
    """Return the video ids in an S3 event: one for each record whose key is under uploads/.

    Each record carries its object's key URL-encoded (a space arrives as +), so decode it with
    unquote_plus first. Ignore keys outside uploads/, such as status/<video_id>.json.
    lambda/test-event.json shows what an event looks like.
    """
    raise NotImplementedError("TODO(task 18): read each record's key and keep the ids under uploads/")


def handler(event: dict, context: object) -> dict:
    """The function's entry point. Floci calls it with an S3 event.

    For each id from video_ids(event): skip it if status/<video_id>.json already exists (a repeat);
    otherwise write status "uploaded" and send one job {"video_id": ..., "key": ...} to reelpipe-jobs.
    Return a small dict that shows what happened, for the invoke output in evidence.md.
    """
    raise NotImplementedError("TODO(task 18): record 'uploaded' and send one job for each new upload")
