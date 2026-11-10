"""MockPay settings, read from environment variables.

Every setting has a default, so MockPay starts with no set-up at all.
The first five fields are the ones the course talks about. The rest are
finer controls: the defaults suit the course, and the tests make them faster.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

# The environment variable behind each setting.
ENV_NAMES = {
    "webhook_secret": "MOCKPAY_WEBHOOK_SECRET",
    "webhook_url": "MOCKPAY_WEBHOOK_URL",
    "duplicate_rate": "MOCKPAY_DUPLICATE_RATE",
    "delay_seconds": "MOCKPAY_DELAY_SECONDS",
    "api_key": "MOCKPAY_API_KEY",
    "late_rate": "MOCKPAY_LATE_RATE",
    "late_max_seconds": "MOCKPAY_LATE_MAX_SECONDS",
    "duplicate_gap_seconds": "MOCKPAY_DUPLICATE_GAP_SECONDS",
    "retry_delays": "MOCKPAY_RETRY_DELAYS",
    "timeout_seconds": "MOCKPAY_TIMEOUT_SECONDS",
    "answer_timeout_seconds": "MOCKPAY_ANSWER_TIMEOUT_SECONDS",
    "public_url": "MOCKPAY_PUBLIC_URL",
    "db_path": "MOCKPAY_DB_PATH",
    "host": "MOCKPAY_HOST",
    "port": "MOCKPAY_PORT",
    "poll_seconds": "MOCKPAY_POLL_SECONDS",
}


@dataclass(frozen=True)
class Settings:
    # --- The settings P6 uses -------------------------------------------
    webhook_secret: str = "mockpay_test_secret"  # shared secret for the HMAC signature
    webhook_url: str = "http://host.docker.internal:8000/payments/webhook"
    duplicate_rate: float = 0.3  # share of webhooks that are sent twice (0 to 1)
    delay_seconds: float = 2.0  # wait before the first try of every webhook
    api_key: str = "mp_test_key"  # the merchant sends it as "Authorization: Bearer ..."

    # --- Finer controls -------------------------------------------------
    late_rate: float = 0.2  # share of webhooks that also get a random extra delay
    late_max_seconds: float = 10.0  # that extra delay is between 0 and this
    duplicate_gap_seconds: float = 3.0  # the copy follows the first by 0 to this
    retry_delays: tuple[float, ...] = (1.0, 5.0, 25.0)  # waits between tries
    timeout_seconds: float = 30.0  # "Pay (times out)" fails after this long
    answer_timeout_seconds: float = 10.0  # how long to wait for the merchant's answer
    public_url: str = "http://localhost:9090"  # the browser's address for MockPay
    db_path: str = "mockpay.db"  # SQLite file
    host: str = "127.0.0.1"  # the Docker image sets 0.0.0.0
    port: int = 9090
    poll_seconds: float = 0.2  # how often the webhook sender looks for work

    def __post_init__(self) -> None:
        for name in ("duplicate_rate", "late_rate"):
            value = getattr(self, name)
            if not 0 <= value <= 1:
                raise ValueError(f"{ENV_NAMES[name]} must be between 0 and 1, not {value}")
        for name in ("delay_seconds", "late_max_seconds", "duplicate_gap_seconds"):
            if getattr(self, name) < 0:
                raise ValueError(f"{ENV_NAMES[name]} must be 0 or more")
        for name in ("timeout_seconds", "answer_timeout_seconds", "poll_seconds"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{ENV_NAMES[name]} must be more than 0")
        if any(delay < 0 for delay in self.retry_delays):
            raise ValueError(f"{ENV_NAMES['retry_delays']} must not contain negative numbers")
        for name in ("webhook_secret", "api_key", "webhook_url"):
            if not getattr(self, name):
                raise ValueError(f"{ENV_NAMES[name]} must not be empty")

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        """Build settings from MOCKPAY_* variables. A missing or empty one keeps its default."""
        env = os.environ if env is None else env
        default = cls()

        def text(name: str) -> str:
            raw = env.get(ENV_NAMES[name], "").strip()
            return raw or getattr(default, name)

        def number(name: str) -> float:
            raw = env.get(ENV_NAMES[name], "").strip()
            if not raw:
                return getattr(default, name)
            try:
                return float(raw)
            except ValueError:
                raise ValueError(f"{ENV_NAMES[name]} must be a number, not {raw!r}") from None

        return cls(
            webhook_secret=text("webhook_secret"),
            webhook_url=text("webhook_url"),
            duplicate_rate=number("duplicate_rate"),
            delay_seconds=number("delay_seconds"),
            api_key=text("api_key"),
            late_rate=number("late_rate"),
            late_max_seconds=number("late_max_seconds"),
            duplicate_gap_seconds=number("duplicate_gap_seconds"),
            retry_delays=_parse_delays(env.get(ENV_NAMES["retry_delays"], ""), default),
            timeout_seconds=number("timeout_seconds"),
            answer_timeout_seconds=number("answer_timeout_seconds"),
            public_url=text("public_url").rstrip("/"),
            db_path=text("db_path"),
            host=text("host"),
            port=int(number("port")),
            poll_seconds=number("poll_seconds"),
        )


def _parse_delays(raw: str, default: Settings) -> tuple[float, ...]:
    """Read a list like "1,5,25" (seconds to wait before each retry)."""
    if not raw.strip():
        return default.retry_delays
    try:
        return tuple(float(part) for part in raw.split(","))
    except ValueError:
        name = ENV_NAMES["retry_delays"]
        raise ValueError(f"{name} must be numbers separated by commas, like 1,5,25") from None
