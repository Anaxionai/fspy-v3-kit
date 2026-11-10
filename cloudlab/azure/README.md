# Azure Storage on your laptop: Azurite

Azurite is Microsoft's emulator for Azure Storage. It runs Blob storage (files, like S3), Queue storage (messages, like SQS) and Table storage. Run every command in Git Bash.

```bash
cd ~/fspy-v3-kit/cloudlab
docker compose --profile azure up -d
```

Blob storage answers on port 10000, Queue storage on 10001 and Table storage on 10002.

## The connection string

A connection string is one line of text with the account name, the key and the addresses. The Azure SDK reads it to find your storage. Azurite uses a fixed development account:

```text
DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;
```

This key is public and the same on every laptop. It works only with Azurite, never with real Azure.

The Azure SDK for Python also accepts a short form that means the same: `UseDevelopmentStorage=true`.

In your app, put the long form in `.env` as `AZURE_STORAGE_CONNECTION_STRING`, and a placeholder in `.env.example`.

## A container and a queue from Python

A container in Blob storage is like a bucket in S3. Save this as `azure_demo.py`:

```python
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueClient

CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
)

# Blob storage: make a container, upload a file, list it and read it back.
blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = blob_service.get_container_client("fspy-lab")
if not container.exists():
    container.create_container()
container.upload_blob("hello.txt", b"hello from Pune", overwrite=True)
print("blobs:", [blob.name for blob in container.list_blobs()])
print("content:", container.download_blob("hello.txt").readall().decode())

# Queue storage: make a queue, send a message, receive it and delete it.
queue = QueueClient.from_connection_string(CONNECTION_STRING, "fspy-lab-queue")
try:
    queue.create_queue()
except ResourceExistsError:
    pass  # the queue is there from an earlier run
queue.send_message("booking 42 confirmed")
for message in queue.receive_messages(max_messages=5):
    print("received:", message.content)
    queue.delete_message(message)
```

Run it:

```bash
uv run --with azure-storage-blob --with azure-storage-queue python azure_demo.py
```

You see:

```text
blobs: ['hello.txt']
content: hello from Pune
received: booking 42 confirmed
```

In your own project, add the packages with `uv add azure-storage-blob azure-storage-queue`.

## An upload link (SAS URL)

A SAS URL (shared access signature) is Azure's version of an S3 presigned URL: a link that allows one action on one blob until it expires. Azurite checks its signature, as Azure does.

```python
from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

blob_service = BlobServiceClient.from_connection_string("UseDevelopmentStorage=true")
sas = generate_blob_sas(
    account_name="devstoreaccount1",
    container_name="fspy-lab",
    blob_name="uploads/ticket.txt",
    account_key=blob_service.credential.account_key,
    permission=BlobSasPermissions(create=True, write=True),
    expiry=datetime.now(timezone.utc) + timedelta(minutes=10),
)
print(f"{blob_service.url}fspy-lab/uploads/ticket.txt?{sas}")
```

Upload with it. Azure needs the `x-ms-blob-type` header:

```bash
curl -X PUT -H "x-ms-blob-type: BlockBlob" --data-binary @hello.txt "PASTE-THE-URL-HERE"
```

## From inside a container

A container cannot reach `127.0.0.1:10000` on your laptop. In the connection string, change each `127.0.0.1` to `host.docker.internal`, and add `extra_hosts: ["host.docker.internal:host-gateway"]` to the service in your `compose.yaml`.

## Troubleshooting

- **`Connection refused`** on port 10000: Azurite is not running. Run `docker ps` and check that `cloudlab-azurite-1` publishes port 10000.
- **`The API version ... is not supported by Azurite`**: the cloud lab starts Azurite with `--skipApiVersionCheck`, which accepts newer SDKs. If you run Azurite another way, add that flag.
- **`ResourceExistsError`** on `create_container` or `create_queue`: it exists from an earlier run. Check with `exists()` first, or catch the error as above.
- **`AuthenticationFailed`** with a SAS URL: the URL changed after it was made, or it expired. Make a new one.
