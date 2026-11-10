# ReelPipe Guided starter (P8, module 10)

This folder is a ready-made `reelpipe/` product folder. It holds the project files, the folder
layout, the settings, the test set-up, the types and the function signatures. The logic is still
yours: every piece a task asks you to write is a stub marked `TODO(task NN)`, where NN is the
task's number in module 10.

## What is included

- `pyproject.toml`, `uv.lock`, `.python-version`: one uv project for the API, the worker and the
  tests (Python 3.12, FastAPI, boto3, the Azure and Google Cloud libraries, and pytest).
- `api/app/`: `main.py` (CORS for the web app, and the four routes as stubs), `status.py`,
  `jobs.py`, and `settings.py` with the fixed names `reelpipe-uploads`, `reelpipe-jobs` and
  `reelpipe-jobs-dlq`.
- `api/app/storage/` and `api/app/queues/`: the `StorageBackend` and `JobQueue` interfaces,
  `UploadTarget` and `Job`, and a stub for every adapter. They wait until task 19.
- `worker/worker.py` (stubs), `worker/Dockerfile` (Python 3.12 slim and uv as in P7; you add ffmpeg in task 10)
  and `compose.yaml` (the worker only: the emulators come from the kit's cloud lab).
- `lambda/handler.py` (stubs), `lambda/deploy.sh` (a skeleton) and `lambda/test-event.json`.
- `aws/setup.sh`, `azure/setup.py` and `gcp/setup.py`: skeletons.
- `tests/`: `conftest.py` (it reads `.env`), `test_smoke.py` (it passes now), and the test files
  of tasks 9, 12, 18, 19 and 22 as skipped stubs.
- `web/`: Vite, React and TypeScript with TanStack Query and Vitest. The upload form, the API
  helper and the types are there, with stubs for task 11.
- `cloud.md`: the six headings and the empty map for task 23.
- `.env.example`, `.gitignore`, `.dockerignore`, and `.gitattributes`, which keeps `.sh` files in
  LF line endings on Windows.

## Copy it in (task 8)

In Git Bash, in task 8's folder, before you make any `reelpipe/` folder:

```bash
git -C ~/fspy-v3-kit pull
cp -r ~/fspy-v3-kit/starters/p08-reelpipe reelpipe
cd reelpipe
cp .env.example .env
uv sync
cd web && npm install && cd ..
```

- Skip step 1 of task 8 (`uv init`, `uv add` and `npm create vite`): the starter has done it.
- Every other `uv add` in the module is done too (task 9 step 8, task 20 step 1, task 21 step 1).
  Running one again changes nothing.
- `.env.example` already holds every setting the module adds (tasks 8, 12, 18, 19, 20 and 21),
  with the emulators' values. Only `GCS_SIGNING_KEY_FILE` waits for you, in task 21.
- Copy the starter only once. Later tasks copy your own `reelpipe/` forward, as their briefs say.

## Run it

From `reelpipe/` in Git Bash:

| What | Command | Notes |
|---|---|---|
| Tests | `uv run pytest -q` | Now: 2 passed, 12 skipped |
| API | `uv run --env-file .env fastapi dev api/app/main.py` | Open http://localhost:8000/docs |
| Web app | `cd web && npm run dev` | Open http://localhost:5173. `npm test` runs its tests |
| AWS set-up | `bash aws/setup.sh` | Start Floci first: `docker compose --profile aws up -d` in `~/fspy-v3-kit/cloudlab` |
| Worker | `docker compose up --build worker` | From task 10 |

A stub fails loudly, and its message names the task that writes it. A route answers 500 and the
API's log shows `NotImplementedError`. The web app shows the error's message.

## TODO map

| Task | Files with a TODO for it |
|---|---|
| 8 | `api/app/main.py` (`POST /uploads`), `web/src/UploadForm.tsx`, `aws/setup.sh` |
| 9 | `api/app/main.py` (`complete`, `GET /videos`, `GET /videos/{video_id}`), `api/app/status.py`, `api/app/jobs.py`, `web/src/UploadForm.tsx`, `aws/setup.sh`, `tests/test_complete.py` |
| 10 | `worker/worker.py` (`main`, `process_job`, `make_thumbnail`, `make_480p`), `worker/Dockerfile` (install ffmpeg), `compose.yaml` (the Floci address) |
| 11 | `web/src/VideoList.tsx`, `StatusBadge.tsx`, `api.ts`, `types.ts`, `UploadForm.tsx`, `VideoList.test.ts` |
| 12 | `worker/worker.py` (`backoff_seconds`, retries, skipping `ready` jobs), `aws/setup.sh`, `tests/test_backoff.py` |
| 18 | `lambda/handler.py`, `lambda/deploy.sh`, `api/app/main.py` (`JOB_TRIGGER`), `tests/test_handler.py` |
| 19 | `api/app/storage/__init__.py`, `storage/s3.py`, `api/app/queues/__init__.py`, `queues/sqs.py`, `api/app/status.py`, `jobs.py`, `main.py`, `worker/worker.py`, `tests/test_backends.py` |
| 20 | `api/app/storage/azure_blob.py`, `storage/__init__.py`, `azure/setup.py`, `tests/test_backends.py` |
| 21 | `api/app/storage/gcs.py`, `api/app/queues/pubsub.py`, both `__init__.py` files, `gcp/setup.py`, `tests/test_backends.py` |
| 22 | `tests/conftest.py`, `tests/test_backends.py` |
| 23 | `cloud.md` |

Task 7 is practice in its own `practice/` folder, and task 24 writes `README.md` and `EXPLAIN.md`,
not code. So neither has a TODO here.

## What you still write yourself

- Every function body marked TODO, and the body of every test. Delete a test's skip line when
  you have written it.
- The JSON files: `aws/cors.json`, `aws/api-policy.json`, `aws/worker-policy.json`,
  `aws/redrive.json`, `lambda/trust-policy.json`, `lambda/role-policy.json` and
  `lambda/notification.json`. JSON cannot hold a TODO comment, so they are not here.
- The commands in `aws/setup.sh` and `lambda/deploy.sh`.
- `evidence.md` and `AI_LOG.md` in your task folders, the content of `cloud.md`, and
  `reelpipe/README.md` and `EXPLAIN.md` in task 24.

## Good to know

- `storage/` and `queues/` wait for task 19. In week 1 you call boto3 directly, as the briefs say.
- For your own `aws` commands, run `export AWS_PROFILE=floci` as well as `AWS_ENDPOINT_URL`: the
  CLI also needs keys and a region (the kit's `cloudlab/aws/README.md`). The scripts set their own.
- In Docker, the worker reaches the emulators on your laptop through `host.docker.internal`.
  `compose.yaml` sets the Azure and Google addresses for the worker (you add Floci's in task 10), so `.env` keeps the `localhost` ones.
- `.gitattributes` keeps `.sh` files in LF. If you make a new `.sh` file, check that the VS Code
  status bar says `LF`, not `CRLF`.
- Put `MSYS_NO_PATHCONV=1` in front of a docker command that names a path inside a container,
  for example `MSYS_NO_PATHCONV=1 docker compose run --rm worker ls /app`.
- Never commit `.env`, `.venv/`, `web/node_modules/` or `function.zip`. `.gitignore` lists them.
- Never copy the kit's Google signing key into `reelpipe/`. Put its path in `.env` as
  `GCS_SIGNING_KEY_FILE` (the kit's `cloudlab/gcp/README.md` makes the key).
