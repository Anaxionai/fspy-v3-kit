# Versions

The tools, images and libraries the course uses, and the version of each.
Briefs never name versions: when a version matters, a task points here.
**Checked on 10 November 2026** against each project's official release page or package registry.

How to read the tables:

- **Pinned** means: use exactly this version. The kit's own files use it, such as `cloudlab/docker-compose.yml`.
- **Course version** means: install this version. A newer patch release (the last number) is fine.
- **Tested** means: the version the course was tested with. Your project's lock file (`uv.lock` or `package-lock.json`) pins the exact version you get.

## On your laptop (Windows)

[`setup/windows.md`](setup/windows.md) installs these.

| Tool | Version | Kind | Notes |
|---|---|---|---|
| Windows | 11, version 23H2 or newer | minimum | Docker Desktop needs 23H2 (build 22631) or newer |
| Git for Windows (Git Bash) | 2.56.0 | course version | Any 2.45 or newer works |
| VS Code | the newest | — | It updates itself |
| uv | 0.13.7 | course version | 0.12 or newer. From uv 0.12, `uv init` makes a packaged `src/` project with no `main.py`; for a flat `main.py` project, use `uv init --no-package --python 3.12 NAME` |
| Python | 3.12.16 | course version | Any 3.12 release. Install it with `uv python install 3.12`; uv's Python is the only Python you need |
| Node.js | 24.22.2 LTS ("Krypton") | course version | v24 or newer. Use the nodejs.org Windows installer and choose v24: `winget install OpenJS.NodeJS.LTS` now gives v26 |
| npm | 11.19.1 | tested | Comes with Node.js 24 |
| Docker Desktop | 4.99.0 | course version | The current release, with the WSL 2 engine. Free under the Personal plan for individual learning, and for small businesses with fewer than 250 employees and less than $10 million in yearly revenue |
| WSL | 2.1.5 or newer | minimum | Check with `wsl --version`; update with `wsl --update` |
| AWS CLI | 2.39.7 | course version | Any 2.x release |

## Cloud lab images

These are pinned in [`cloudlab/docker-compose.yml`](cloudlab/docker-compose.yml). Do not change them in your own copy.

| Service | Image | Kind | Notes |
|---|---|---|---|
| PostgreSQL 16 with pgvector | `pgvector/pgvector:0.8.7-pg16` | pinned | PostgreSQL 16.15 and pgvector 0.8.7, from the `pgvector/pgvector:pg16` line |
| Redis 7 | `redis:7.4.12-alpine` | pinned | |
| MongoDB 7 | `mongo:7.0.45` | pinned | |
| Mailpit | `axllent/mailpit:v1.33.1` | pinned | |
| Floci (AWS emulator) | `floci/floci:2.4.0` | pinned | MIT licence, no account needed. The `-compat` tags add the AWS CLI inside the container; the course does not need them |
| Azurite (Azure Storage emulator) | `mcr.microsoft.com/azure-storage/azurite:3.37.0` | pinned | |
| fake-gcs-server (Google Cloud Storage emulator) | `fsouza/fake-gcs-server:1.56.1` | pinned | |
| Google Cloud CLI emulators (Pub/Sub) | `gcr.io/google.com/cloudsdktool/google-cloud-cli:592.0.0-emulators` | pinned | |
| Toxiproxy | `ghcr.io/shopify/toxiproxy:2.13.0` | pinned | |

## Kubernetes and infrastructure as code

| Tool | Version | Kind | Notes |
|---|---|---|---|
| k3d | 5.9.0 | course version | `winget install -e --id k3d.k3d --version 5.9.0` (its default cluster image is k3s 1.35.5) |
| k3s (inside k3d) | `rancher/k3s:v1.35.5-k3s1` | pinned | k3d 5.9.0's default image |
| kubectl | 1.35.4 | course version | kubectl supports a cluster one minor version older or newer, so it is pinned next to k3s 1.35: `winget install -e --id Kubernetes.kubectl --version 1.35.4` |
| Helm | 4.3.1 | course version | `winget install -e --id Helm.Helm --version 4.3.1`. The course's Helm commands work the same in Helm 3 and Helm 4 |
| OpenTofu | 1.13.9 | course version | 1.8 or newer. `winget install -e --id OpenTofu.Tofu` |
| `hashicorp/aws` provider | 6.72.0 | pinned | In `main.tf`: `version = "6.72.0"` inside `required_providers` |

## Testing, security and CI

| Tool | Version | Kind | Notes |
|---|---|---|---|
| k6 | 2.3.0 | course version | `winget install -e --id GrafanaLabs.k6`, or the image `grafana/k6:2.3.0` |
| Playwright | 1.65.0 | course version | The npm package `@playwright/test`, and `playwright` for Python |
| Trivy | 0.76.2 | pinned | Run it as the image `aquasec/trivy:0.76.2` |
| act | 0.2.97 | course version | Runs GitHub Actions workflows on your laptop. `winget install -e --id nektos.act` |
| FFmpeg | 9.0.2 | course version | `winget install -e --id Gyan.FFmpeg` on Windows. Inside `python:3.12-slim` images, `apt-get install ffmpeg` gives 7.1, which also works |

### GitHub Actions

Use these major versions in workflow files, written as `uses: name@version`:

| Action | Version |
|---|---|
| `actions/checkout` | `v7` |
| `actions/setup-python` | `v7` |
| `actions/setup-node` | `v7` |
| `astral-sh/setup-uv` | `v10.3.3` (a full tag: setup-uv no longer publishes a moving `v10` tag) |
| `actions/cache` | `v6` |
| `actions/upload-artifact` | `v7` |
| `opentofu/setup-opentofu` | `v2` |
| `docker/setup-buildx-action` | `v4` |
| `docker/login-action` | `v4` |
| `docker/metadata-action` | `v6` |
| `docker/build-push-action` | `v7` |

Run jobs on `runs-on: ubuntu-24.04`.

## Images for your own Dockerfiles and Compose files

| Use | Image | Kind |
|---|---|---|
| Python services | `python:3.12-slim` (now `python:3.12.16-slim-trixie`) | course version |
| Building a web front end | `node:24-alpine` (now `node:24.22.2-alpine`) | course version |
| Serving a built front end | `nginx:1.30.6-alpine` | pinned |
| Prometheus | `prom/prometheus:v3.16.0` | pinned |
| Grafana | `grafana/grafana:13.3.0` | pinned |
| Local image registry for k3d | `registry:2` | pinned |

## Python libraries

Add them with `uv add`, for example `uv add "fastapi==0.162.2"` to pin one.

| Package | Tested | Notes |
|---|---|---|
| `fastapi` | 0.162.2 | Built-in Server-Sent Events (`fastapi.sse.EventSourceResponse`) arrived in 0.135.0; use 0.135.0 or newer |
| `uvicorn` | 0.54.0 | Comes with `fastapi[standard]` |
| `pydantic` | 2.14.3 | |
| `pydantic-settings` | 2.16.2 | |
| `sqlalchemy` | 2.1.8 | The SQLAlchemy 2 style, with `asyncio` |
| `asyncpg` | 0.32.0 | |
| `psycopg` | 3.3.8 | |
| `alembic` | 1.20.1 | |
| `pgvector` | 0.5.1 | The Python package for the `vector` type |
| `httpx` | 0.28.1 | |
| `pytest` | 9.2.0 | |
| `pytest-asyncio` | 1.4.1 | |
| `ruff` | 0.17.4 | |
| `mypy` | 2.4.1 | |
| `typer` | 0.29.0 | |
| `rich` | 15.0.0 | |
| `celery` | 5.7.0 | |
| `redis` | 8.1.0 | The Python client; the server is Redis 7 |
| `pymongo` | 4.19.0 | |
| `boto3` | 1.43.127 | |
| `azure-storage-blob` | 12.31.1 | |
| `google-cloud-storage` | 3.17.1 | |
| `google-cloud-pubsub` | 2.43.0 | |
| `google-genai` | 3.0.0 | The Gemini API library; models are in `data/railseat/ask-railseat.md` |
| `pyjwt` | 2.15.1 | |
| `pwdlib` | 0.3.1 | Password hashing, with `pwdlib[argon2]` |
| `email-validator` | 2.3.0 | |
| `websockets` | 17.4 | |
| `prometheus-client` | 0.26.0 | |
| `opentelemetry-sdk` | 1.45.2 | |
| `opentelemetry-instrumentation-fastapi` | 0.66b2 | |

## npm packages

Add them with `npm install`, for example `npm install leaflet@1.9.4` to pin one.

| Package | Tested | Notes |
|---|---|---|
| `vite` | 8.3.7 | `npm create vite@latest` uses `create-vite` 9.3.4 |
| `react`, `react-dom` | 19.3.1 | |
| `typescript` | 7.0.2 | Vite's React template asks for `~7.0.2` |
| `@vitejs/plugin-react` | 6.3.0 | |
| `vitest` | 5.1.0 | |
| `@playwright/test` | 1.65.0 | |
| `recharts` | 3.10.1 | |
| `@tanstack/react-query` | 5.107.1 | |
| `react-router` | 8.5.1 | |
| `zod` | 4.6.7 | |
| `tailwindcss`, `@tailwindcss/vite` | 4.3.5 | |
| `leaflet` | **1.9.4** (pinned) | `npm install leaflet` gives 1.9.4. The Leaflet website teaches the 2.0 beta, whose code is different: follow the 1.9.4 reference |
| `@types/leaflet` | 1.9.22 | |
| `tsx` | 4.23.15 | |
