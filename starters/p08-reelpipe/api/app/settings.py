"""ReelPipe's fixed names. They are the same in every task and on every cloud.

Import them instead of typing the strings again, so a typing mistake cannot creep in:
    from app.settings import BUCKET, QUEUE
Settings that change between runs (STORAGE_BACKEND, JOB_TRIGGER and the rest) come from .env.
"""

BUCKET = "reelpipe-uploads"  # the S3 bucket, the Azure container and the Cloud Storage bucket
QUEUE = "reelpipe-jobs"  # the SQS queue (task 9) and the Pub/Sub topic (task 21)
DLQ = "reelpipe-jobs-dlq"  # the dead-letter queue (task 12) and the dead-letter topic (task 21)
SUBSCRIPTION = "reelpipe-jobs-sub"  # the Pub/Sub subscription the worker pulls from (task 21)
