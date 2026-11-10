# Google Cloud on your laptop: fake-gcs-server and the Pub/Sub emulator

The `gcp` profile starts two emulators:

- fake-gcs-server, which imitates Cloud Storage (buckets and files) at `http://localhost:4443`;
- the Pub/Sub emulator from Google, which imitates Pub/Sub (topics and subscriptions) at `localhost:8085`.

Run every command in Git Bash.

```bash
cd ~/fspy-v3-kit/cloudlab
docker compose --profile gcp up -d
curl -s http://localhost:8085
```

The last command prints `Ok`. Neither emulator checks credentials, and nothing reaches the real Google Cloud.

## The settings

| Variable | Value | Read by |
|---|---|---|
| `STORAGE_EMULATOR_HOST` | `http://localhost:4443` | `google-cloud-storage`: with it set, the client uses the emulator and no credentials |
| `PUBSUB_EMULATOR_HOST` | `localhost:8085` | `google-cloud-pubsub`: with it set, every call goes to the emulator |
| `GCS_SIGNING_KEY_FILE` | the path that `make_signing_key.py` prints | your own code, to sign upload URLs (see below) |

Put them in your app's `.env`. In a terminal, `export PUBSUB_EMULATOR_HOST=localhost:8085` sets one until you close that terminal.

## Cloud Storage from Python

Save this as `gcs_demo.py`. It gives the client anonymous credentials and the emulator's address (`api_endpoint`):

```python
from google.api_core.exceptions import Conflict
from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

client = storage.Client(
    project="fspy-local",                 # any name works on the emulator
    credentials=AnonymousCredentials(),   # the emulator does not check credentials
    client_options={"api_endpoint": "http://localhost:4443"},
)

try:
    bucket = client.create_bucket("fspy-lab-bucket")
except Conflict:                          # the bucket is there from an earlier run
    bucket = client.bucket("fspy-lab-bucket")

blob = bucket.blob("hello.txt")
blob.upload_from_string("hello from Pune", content_type="text/plain")
print("objects:", [b.name for b in client.list_blobs("fspy-lab-bucket")])
print("content:", blob.download_as_text())
```

Run it:

```bash
uv run --with google-cloud-storage python gcs_demo.py
```

It prints `objects: ['hello.txt']` and `content: hello from Pune`. In your own project, add the package with `uv add google-cloud-storage`.

With `STORAGE_EMULATOR_HOST` set, `storage.Client(project="fspy-local")` alone does the same: the client then uses the emulator and anonymous credentials.

## Signed upload URLs (V4)

A signed URL is Google's version of an S3 presigned URL. The client can only sign with a service account key, and the emulator's anonymous credentials have none. So you make a throwaway key on your laptop.

The key is fake and works only with the emulator. It is made on your laptop and never committed.

```bash
cd ~/fspy-v3-kit/cloudlab/gcp
uv run --with cryptography python make_signing_key.py
```

It writes `.signing-key.json` in that folder and prints its full path. The cloud lab's `.gitignore` keeps the file out of Git. Copy the printed path into your `.env` as `GCS_SIGNING_KEY_FILE`.

Sign a PUT URL for one file:

```python
import os
from datetime import timedelta
from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from google.oauth2 import service_account

client = storage.Client(project="fspy-local", credentials=AnonymousCredentials(),
                        client_options={"api_endpoint": "http://localhost:4443"})
signer = service_account.Credentials.from_service_account_file(os.environ["GCS_SIGNING_KEY_FILE"])

blob = client.bucket("fspy-lab-bucket").blob("uploads/video-1.mp4")
upload_url = blob.generate_signed_url(
    version="v4",
    method="PUT",
    expiration=timedelta(minutes=10),
    content_type="video/mp4",
    credentials=signer,                          # the throwaway key signs the URL
    api_access_endpoint="http://localhost:4443", # the URL points at the emulator
)
print(upload_url)
```

Upload with it, sending the same `Content-Type` that you signed:

```bash
curl -X PUT -H "Content-Type: video/mp4" --data-binary @my-video.mp4 "PASTE-THE-URL-HERE"
```

- The emulator matches signed uploads only on the host `localhost:4443`. The cloud lab starts it with `-public-host localhost:4443` for this reason.
- The emulator does not check the signature, the expiry or the content type. Real Google Cloud does.
- The emulator answers browser CORS checks for `PUT`, so a web page on `localhost:5173` can upload with the URL.

## Pub/Sub from Python

A topic receives messages. Each subscription on the topic gets its own copy of every message. Save this as `pubsub_demo.py`:

```python
import os
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

os.environ.setdefault("PUBSUB_EMULATOR_HOST", "localhost:8085")  # send every call to the emulator
PROJECT = "fspy-local"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(PROJECT, "fspy-lab-topic")
subscription_path = subscriber.subscription_path(PROJECT, "fspy-lab-sub")

try:
    publisher.create_topic(name=topic_path)
except AlreadyExists:
    pass
try:
    subscriber.create_subscription(name=subscription_path, topic=topic_path)
except AlreadyExists:
    pass

future = publisher.publish(topic_path, b"booking 42 confirmed", city="Pune")
print("published message id:", future.result())

response = subscriber.pull(subscription=subscription_path, max_messages=5, timeout=10)
for received in response.received_messages:
    print("received:", received.message.data.decode(), dict(received.message.attributes))
if response.received_messages:
    subscriber.acknowledge(subscription=subscription_path,
                           ack_ids=[m.ack_id for m in response.received_messages])
```

Run it:

```bash
uv run --with google-cloud-pubsub python pubsub_demo.py
```

It prints the message ID, then `received: booking 42 confirmed {'city': 'Pune'}`. An acknowledged message is not delivered again.

The emulator keeps nothing when it stops. After each start, create your topics and subscriptions again, for example with a `setup.py` script in your project.

## From inside a container

A container cannot reach `localhost` on your laptop. Use `http://host.docker.internal:4443` for `STORAGE_EMULATOR_HOST` and `host.docker.internal:8085` for `PUBSUB_EMULATOR_HOST`. Add `extra_hosts: ["host.docker.internal:host-gateway"]` to the service in your `compose.yaml`.

## Troubleshooting

- **`DefaultCredentialsError`**: the client looked for real Google credentials. Pass `credentials=AnonymousCredentials()` and `api_endpoint`, or set `STORAGE_EMULATOR_HOST`.
- **Pub/Sub fails with `DefaultCredentialsError`**: `PUBSUB_EMULATOR_HOST` is not set in that process, so the client looked for the real Google Cloud.
- **`NotFound` for a topic or subscription**: the emulator restarted and forgot it. Create it again.
- **A signed `PUT` returns 404**: the URL host is not `localhost:4443`. Pass `api_access_endpoint="http://localhost:4443"`.
- **`FileNotFoundError` for the key**: run `make_signing_key.py` again, and copy the path it prints into `GCS_SIGNING_KEY_FILE`.
