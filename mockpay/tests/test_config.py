"""Settings from environment variables."""

import pytest

from mockpay.config import Settings


def test_defaults_match_the_course() -> None:
    settings = Settings.from_env({})

    assert settings.webhook_secret == "mockpay_test_secret"
    assert settings.webhook_url == "http://host.docker.internal:8000/payments/webhook"
    assert settings.duplicate_rate == 0.3
    assert settings.delay_seconds == 2.0
    assert settings.api_key == "mp_test_key"
    assert settings.late_rate == 0.2
    assert settings.late_max_seconds == 10.0
    assert settings.retry_delays == (1.0, 5.0, 25.0)
    assert settings.timeout_seconds == 30.0
    assert settings.port == 9090


def test_values_come_from_the_environment() -> None:
    settings = Settings.from_env(
        {
            "MOCKPAY_WEBHOOK_SECRET": "s3cret",
            "MOCKPAY_WEBHOOK_URL": "http://localhost:8000/payments/webhook",
            "MOCKPAY_DUPLICATE_RATE": "1",
            "MOCKPAY_DELAY_SECONDS": "0",
            "MOCKPAY_API_KEY": "mp_other",
            "MOCKPAY_RETRY_DELAYS": "1, 2,3",
            "MOCKPAY_TIMEOUT_SECONDS": "5",
            "MOCKPAY_PUBLIC_URL": "http://localhost:9091/",
        }
    )

    assert settings.webhook_secret == "s3cret"
    assert settings.webhook_url == "http://localhost:8000/payments/webhook"
    assert settings.duplicate_rate == 1.0
    assert settings.delay_seconds == 0.0
    assert settings.api_key == "mp_other"
    assert settings.retry_delays == (1.0, 2.0, 3.0)
    assert settings.timeout_seconds == 5.0
    assert settings.public_url == "http://localhost:9091"


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("MOCKPAY_DUPLICATE_RATE", "1.5"),
        ("MOCKPAY_DUPLICATE_RATE", "lots"),
        ("MOCKPAY_DELAY_SECONDS", "-1"),
        ("MOCKPAY_RETRY_DELAYS", "1,five"),
        ("MOCKPAY_TIMEOUT_SECONDS", "0"),
    ],
)
def test_bad_values_stop_mockpay_with_a_clear_message(name: str, value: str) -> None:
    with pytest.raises(ValueError, match=name):
        Settings.from_env({name: value})
