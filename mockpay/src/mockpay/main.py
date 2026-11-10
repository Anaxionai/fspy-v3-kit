"""The `mockpay` command: reads the settings and starts the web server."""

import logging
from datetime import datetime

import uvicorn

from mockpay import __version__, clock
from mockpay.app import create_app
from mockpay.config import Settings


class IstFormatter(logging.Formatter):
    """Log times in IST, like the API and the dashboard. (A container's clock is UTC.)"""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        return datetime.fromtimestamp(record.created, clock.IST).strftime(datefmt or "%H:%M:%S")


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(IstFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    # httpx would log every webhook request again; MockPay logs each attempt itself.
    logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    try:
        settings = Settings.from_env()
    except ValueError as exc:
        raise SystemExit(f"MockPay cannot start: {exc}") from None

    setup_logging()
    log = logging.getLogger("mockpay")
    log.info("MockPay %s. Dashboard: %s/dashboard", __version__, settings.public_url)
    log.info("API docs: %s/docs", settings.public_url)
    log.info(
        "Webhooks go to %s (sent twice: %g%%, delay: %g s)",
        settings.webhook_url,
        settings.duplicate_rate * 100,
        settings.delay_seconds,
    )
    if settings.webhook_secret == Settings.webhook_secret:
        log.info("Using the default test secret. Fine for learning, never for real money.")

    uvicorn.run(create_app(settings), host=settings.host, port=settings.port)
