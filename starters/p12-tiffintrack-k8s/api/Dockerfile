# The TiffinTrack API image (task 8). Build it from the tiffintrack/ folder:
#   docker build -f api/Dockerfile -t tiffintrack-api:0.1.0 .

# Build stage: install the locked dependencies into /app/.venv.
FROM python:3.12 AS build
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /bin/uv
WORKDIR /app
# Compile to bytecode now. The final image runs as a user who cannot write it, and
# without it every start is slow, which can fail the probes in task 21.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Final stage: a slim image with the dependencies and the API's code only.
FROM python:3.12-slim
WORKDIR /app
# The official Python images ship without the standard library's bytecode: compile it once here.
RUN python -m compileall -q /usr/local/lib/python3.12 && useradd --create-home tiffin
COPY --from=build /app/.venv /app/.venv
COPY api ./api
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER tiffin
EXPOSE 8000
CMD ["fastapi", "run", "api/app/main.py", "--port", "8000"]
