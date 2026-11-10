#!/usr/bin/env bash
# Smoke test for a running Shortly stack (task 14): a quick check that the main path works.
# Run it from shortly/ while the stack runs:  bash scripts/smoke.sh
# It must exit 0 when every check passes, and non-zero on the first failure.
set -euo pipefail

# The API's address. Another address for one run: BASE_URL=http://host:port bash scripts/smoke.sh
BASE_URL="${BASE_URL:-http://localhost:8080}"
TARGET="https://en.wikipedia.org/wiki/Pune"

# TODO(task 14): wait up to 60 seconds for the API: try GET $BASE_URL/healthz once a second
#   until it answers 200. If it never does, print a message and exit 1.

# TODO(task 14): create a link with POST $BASE_URL/links and the JSON body {"target_url": "$TARGET"}.
#   Exit 1 unless the status is 201, then read the code from the answer.
#   jq is not in Git Bash on Windows: read the code with grep -o or sed instead.

# TODO(task 14): request $BASE_URL/<code> without following the redirect. Exit 1 unless the
#   status is 302 and the Location header is $TARGET. Then print a pass message.

echo "TODO(task 14): write the smoke test" >&2
exit 1
