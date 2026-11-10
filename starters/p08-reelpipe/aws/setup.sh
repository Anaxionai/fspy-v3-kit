#!/usr/bin/env bash
# Rebuild ReelPipe's AWS resources on Floci in one go. Run it from reelpipe/ in Git Bash:
#   bash aws/setup.sh
# Floci must be running: `docker compose --profile aws up -d` in the kit's cloudlab/ folder.

# Talk to Floci, never to a real AWS account, even in a new terminal.
export AWS_ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://localhost:4566}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-ap-south-1}"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"

# Work in reelpipe/, so file://aws/cors.json and the other files are found.
cd "$(dirname "$0")/.."

# TODO(task 8): make the bucket reelpipe-uploads, then apply the CORS rules in aws/cors.json.
# TODO(task 9): create the queue reelpipe-jobs with a 120-second visibility timeout.
# TODO(task 12): create reelpipe-jobs-dlq, then set the redrive policy in aws/redrive.json on reelpipe-jobs.
