# ReelPipe's worker: Python 3.12, ffmpeg, and the packages in uv.lock.
# The build context is reelpipe/ (see compose.yaml). From reelpipe/ run:
#   docker compose up --build worker

# ---- Build stage: install the exact packages from uv.lock with uv, as in P7 ----
FROM python:3.12-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app

# The packages first: Docker keeps this layer until pyproject.toml or uv.lock changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Then ReelPipe's code. The worker imports app.status (and later app.storage and app.queues) from api/.
COPY api ./api
COPY worker ./worker

# ---- Final stage: slim Python with ffmpeg ----
FROM python:3.12-slim

# TODO(task 10): install ffmpeg in this stage with apt-get, as you did in task 5's container.
# Keep the image small: no recommended extras, and remove apt's package lists in the same RUN.

WORKDIR /app
COPY --from=build /app /app

# Run as a normal user, not root.
RUN useradd --create-home reelpipe
USER reelpipe

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/api \
    PYTHONUNBUFFERED=1

CMD ["python", "worker/worker.py"]
