"""Create ReelPipe's bucket, topics and subscriptions on Google's emulators (task 21).
Run it from reelpipe/ in Git Bash:

    uv run --env-file .env python gcp/setup.py

The emulators must be running: `docker compose --profile gcp up -d` in the kit's cloudlab/ folder.
"""


def main() -> None:
    """Create everything ReelPipe needs on fake-gcs-server and the Pub/Sub emulator.

    - the bucket reelpipe-uploads;
    - the topics reelpipe-jobs and reelpipe-jobs-dlq;
    - the subscription reelpipe-jobs-sub on reelpipe-jobs, with a 120-second ack deadline and a
      dead-letter policy to reelpipe-jobs-dlq after 5 delivery attempts;
    - a subscription on reelpipe-jobs-dlq, so the dead letters are kept.
    The project id is in GOOGLE_CLOUD_PROJECT. Keep anything that exists already, so you can run this again.
    """
    raise NotImplementedError("TODO(task 21): create the bucket, both topics and the subscriptions")


if __name__ == "__main__":
    main()
