# AWS on your laptop: Floci

Floci is a free AWS emulator (a program that imitates AWS). It answers AWS API calls at `http://localhost:4566`, so the AWS CLI, `boto3` and OpenTofu work against it. Nothing costs money, and nothing reaches the real AWS.

Floci runs S3, SQS, Lambda, IAM, STS and Budgets, and more. Its fake account ID is `000000000000`.

Run every command in Git Bash. Work in a folder of your own, for example `~/fspy/floci-practice`, not inside the kit.

## 1. Start Floci

```bash
cd ~/fspy-v3-kit/cloudlab
docker compose --profile aws up -d
curl -s http://localhost:4566/_floci/health
```

The last command prints JSON that contains `"version":"2.4.0"`.

The `aws` profile mounts the Docker socket (`/var/run/docker.sock`), which lets Floci start Docker containers. Floci needs it for Lambda: it runs each function in its own container. With Docker Desktop on Windows, this works as written in `docker-compose.yml`.

Floci keeps buckets, queues, functions and budgets when you stop it with `down`. `docker compose --profile aws down -v` deletes them all.

## 2. Install the AWS CLI v2

```bash
winget install -e --id Amazon.AWSCLI
```

Close VS Code and open it again, so Git Bash finds the new `aws` command. Then check:

```bash
aws --version
```

It prints `aws-cli/2.` followed by the version. Use 2.32 or later.

## 3. Make the `floci` profile

A profile (a named set of settings) keeps Floci's fake keys apart from a real AWS account. Run:

```bash
aws configure --profile floci
```

Answer the four questions like this:

```text
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: ap-south-1
Default output format [None]: json
```

Then add Floci's address to the profile:

```bash
aws configure set endpoint_url http://localhost:4566 --profile floci
```

Check the result with `cat ~/.aws/config`. It must contain:

```ini
[profile floci]
region = ap-south-1
output = json
endpoint_url = http://localhost:4566
```

The keys are in `~/.aws/credentials`, under `[floci]`. They are fake, so they are safe on your laptop. Never put real AWS keys in this profile.

Check that you reach Floci:

```bash
aws sts get-caller-identity --profile floci
```

The `Account` is `000000000000`. If you see any other 12-digit number, you reached a real AWS account: stop and check your profile.

### Three ways to send a command to Floci

| Way | Example | When to use it |
|---|---|---|
| `--profile floci` on each command | `aws s3 ls --profile floci` | the examples in this file |
| `AWS_PROFILE` for the whole terminal | `export AWS_PROFILE=floci`, then `aws s3 ls` | a long session of commands |
| Environment variables | see below | your app's `.env`, and tasks that say `export AWS_ENDPOINT_URL` |

The environment variable way:

```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=ap-south-1
export AWS_ENDPOINT_URL=http://localhost:4566
```

`AWS_ENDPOINT_URL` alone is not enough: the CLI also needs keys and a region. Either `export AWS_PROFILE=floci` or the three other lines above give it them. `boto3` reads the same variables. An `export` lasts until you close that terminal.

You can also give the address on one command: `aws --endpoint-url http://localhost:4566 --profile floci s3 ls`.

## 4. A bucket (S3)

```bash
aws s3 mb s3://fspy-lab-bucket --profile floci
echo "hello from Pune" > hello.txt
aws s3 cp hello.txt s3://fspy-lab-bucket/hello.txt --profile floci
aws s3 ls s3://fspy-lab-bucket/ --profile floci
```

The last command lists `hello.txt` with its size, 16 bytes. After you make a Lambda function, `aws s3 ls` also shows a bucket named `awslambda-ap-south-1-tasks`. Floci keeps function code there. Leave it alone.

## 5. A queue (SQS)

```bash
aws sqs create-queue --queue-name fspy-lab-queue --profile floci
```

It prints the queue's address, its `QueueUrl`: `http://localhost:4566/000000000000/fspy-lab-queue`. Keep it in a variable, then send and receive a message:

```bash
QUEUE_URL=$(aws sqs get-queue-url --queue-name fspy-lab-queue --profile floci --query QueueUrl --output text)
aws sqs send-message --queue-url "$QUEUE_URL" --message-body "booking 42 confirmed" --profile floci
aws sqs receive-message --queue-url "$QUEUE_URL" --wait-time-seconds 2 --profile floci
```

Find your text in `Body`. A received message stays in the queue until you delete it with its `ReceiptHandle`:

```bash
aws sqs delete-message --queue-url "$QUEUE_URL" --receipt-handle "PASTE-THE-ReceiptHandle-HERE" --profile floci
```

If you do not delete it, the message comes back after the visibility timeout (30 seconds by default).

## 6. A presigned URL from Python

A presigned URL is a link that allows one action on one object until it expires. Save this as `presign.py`:

```python
import boto3
from botocore.config import Config

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",  # Floci. Leave this out for real AWS.
    region_name="ap-south-1",
    aws_access_key_id="test",              # Floci's fake keys. In your app, read
    aws_secret_access_key="test",          # all four values from environment variables.
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)

upload_url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": "fspy-lab-bucket", "Key": "uploads/ticket.txt"},
    ExpiresIn=600,  # seconds: the link works for 10 minutes
)
download_url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": "fspy-lab-bucket", "Key": "uploads/ticket.txt"},
    ExpiresIn=600,
)
print(upload_url)
print(download_url)
```

Run it, then upload and download with the two links:

```bash
uv run --with boto3 python presign.py
curl -X PUT --upload-file hello.txt "PASTE-THE-FIRST-URL-HERE"
curl "PASTE-THE-SECOND-URL-HERE"
```

The second `curl` prints `hello from Pune`. In your own project, add the package with `uv add boto3` instead of `--with boto3`.

- If you add `ContentType` to `Params`, the upload must send the same `Content-Type` header.
- When a link has expired, Floci answers `403` with `Request has expired.`, as AWS does.
- Floci does not check the signature itself. Real AWS does, so test a signature mistake on real AWS only.

## 7. A Lambda function from a zip file

Save this as `handler.py`:

```python
def handler(event, context):
    city = event.get("city", "Pune")
    return {"message": f"Hello from Lambda in {city}!"}
```

Save this as `trust-policy.json`. It lets the Lambda service use the role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Save this as `event.json`:

```json
{"city": "Mumbai"}
```

Zip the code, make the role, and make the function:

```bash
uv run python -m zipfile -c function.zip handler.py
aws iam create-role --role-name fspy-lambda-role --assume-role-policy-document file://trust-policy.json --profile floci
aws lambda create-function --function-name fspy-hello --runtime python3.12 --handler handler.handler --role arn:aws:iam::000000000000:role/fspy-lambda-role --zip-file fileb://function.zip --profile floci
aws lambda wait function-active-v2 --function-name fspy-hello --profile floci
```

Call it and read the answer:

```bash
aws lambda invoke --function-name fspy-hello --cli-binary-format raw-in-base64-out --payload file://event.json response.json --profile floci
cat response.json
```

`response.json` contains `{"message": "Hello from Lambda in Mumbai!"}`.

- The first call downloads the Python 3.12 Lambda image (about 190 MB). It can take 2 minutes. Later calls take 1 to 2 seconds.
- While a function runs, `docker ps` shows a container named `floci-aws-fspy-hello-...`. Floci removes idle ones after 2 minutes.
- Floci gives every function the variable `AWS_ENDPOINT_URL`. A plain `boto3.client("sqs")` inside your function reaches Floci with no extra settings.

## 8. Clean up

```bash
aws lambda delete-function --function-name fspy-hello --profile floci
aws iam delete-role --role-name fspy-lambda-role --profile floci
aws sqs delete-queue --queue-url "$QUEUE_URL" --profile floci
aws s3 rb s3://fspy-lab-bucket --force --profile floci
```

To delete everything in Floci at once: `docker compose --profile aws down -v` in the cloud lab folder.

## From inside a container

A container cannot reach `localhost:4566` on your laptop. Give it `AWS_ENDPOINT_URL=http://host.docker.internal:4566` and `extra_hosts: ["host.docker.internal:host-gateway"]` in your `compose.yaml`. `boto3` sends SQS calls to that address even when a `QueueUrl` says `localhost`.

## Troubleshooting

- **`Could not connect to the endpoint URL`**: Floci is not running. Start it with `docker compose --profile aws up -d` in the cloud lab folder.
- **`Unable to locate credentials`**: the command has no keys. Add `--profile floci`, or run `export AWS_PROFILE=floci` in this terminal.
- **`InvalidClientTokenId`** or any error that names a real account: the command missed Floci's address and went to the real AWS. Check `cat ~/.aws/config`, and add `--profile floci`.
- **A Docker error when you create or call a function**: Floci cannot reach the Docker socket. Check that Docker Desktop runs, then restart Floci with `docker compose --profile aws down` and `docker compose --profile aws up -d`.
- **The first `invoke` times out**: the Lambda image is still downloading. Wait 2 minutes and call it again.
- **`aws: command not found`**: close VS Code and open it again after the install, or reinstall with `winget`.
