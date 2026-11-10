# Shortly's image. One image runs both the API and (from task 19) the Celery worker.
# Build it from shortly/:  docker build -t shortly-api .
#
# An outline: write each TODO with the steps of task 8, as in your practice Dockerfile (task 6).

# ---- Stage 1: build. The full Python image, with uv. It installs the dependencies into /app/.venv.
FROM python:3.12 AS build
# TODO(task 8): copy uv in from its image (the tag is in the kit's VERSIONS.md).
WORKDIR /app
# TODO(task 8): copy api/pyproject.toml and api/uv.lock, then install the dependencies
#   with `uv sync --locked --no-dev`. Do this before you copy any application code.
#   Tip: `ENV UV_COMPILE_BYTECODE=1` before `uv sync` makes the container start faster
#   (see "Using uv in Docker").

# ---- Stage 2: final. The slim image: no uv and no build tools, only the .venv and the code.
FROM python:3.12-slim
WORKDIR /app
# TODO(task 8): copy /app/.venv from the build stage, then api/app, api/alembic and api/alembic.ini.
# TODO(task 19): copy worker/ as well, after the API code, so this image can also run the worker.
# TODO(task 8): put /app/.venv/bin first on PATH.
# TODO(task 8): create a user named shortly and switch to it, so the app does not run as root.
# TODO(task 8): expose port 8080. End with a CMD that runs `alembic upgrade head`, then
#   uvicorn for app.main:app on host 0.0.0.0, port 8080.
