# MockPay: Python 3.12 and the app, listening on port 9090.
FROM python:3.12-slim

# uv installs the exact package versions listed in uv.lock.
COPY --from=ghcr.io/astral-sh/uv:0.12.8 /uv /bin/uv

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# 1. The dependencies only. Docker keeps this layer until uv.lock changes,
#    so changing MockPay's code does not download everything again.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 2. MockPay itself.
COPY README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

# Run as a normal user, not root. The SQLite file lives in /data (a volume).
RUN useradd --create-home mockpay && mkdir /data && chown mockpay /data
USER mockpay

ENV PATH="/app/.venv/bin:$PATH" \
    MOCKPAY_HOST=0.0.0.0 \
    MOCKPAY_PORT=9090 \
    MOCKPAY_DB_PATH=/data/mockpay.db

EXPOSE 9090
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:9090/health', timeout=2)"]

CMD ["mockpay"]
