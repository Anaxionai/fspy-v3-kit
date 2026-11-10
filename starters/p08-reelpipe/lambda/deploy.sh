#!/usr/bin/env bash
# Deploy ReelPipe's Lambda function on Floci (task 18). Run it from reelpipe/ in Git Bash:
#   bash lambda/deploy.sh
# Floci must be running with the Docker socket, as the kit's cloudlab/aws/README.md says.

# Talk to Floci, never to a real AWS account, even in a new terminal.
export AWS_ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://localhost:4566}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-ap-south-1}"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"

# Work inside lambda/, so handler.py and the JSON files are found by their short names.
cd "$(dirname "$0")"

# TODO(task 18): create the role reelpipe-on-upload from trust-policy.json (aws iam create-role),
#   then give it role-policy.json (aws iam put-role-policy).
# TODO(task 18): zip handler.py into function.zip, then create the function with
#   aws lambda create-function: runtime python3.12, handler handler.handler, the role's ARN.
# TODO(task 18): let S3 call the function (aws lambda add-permission), then apply
#   notification.json to the bucket (aws s3api put-bucket-notification-configuration).
