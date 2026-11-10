from collections.abc import Callable, Iterator
from contextlib import ExitStack
from itertools import count
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mockpay.app import create_app
from mockpay.config import Settings
from tests.helpers import WebhookReceiver, fast_settings


@pytest.fixture
def receiver() -> Iterator[WebhookReceiver]:
    """A local server that receives MockPay's webhooks during a test."""
    server = WebhookReceiver()
    server.start()
    yield server
    server.stop()


@pytest.fixture
def make_client(tmp_path: Path, receiver: WebhookReceiver) -> Iterator[Callable[..., TestClient]]:
    """Start MockPay with fast test settings. Keyword arguments change single settings.

    The `with TestClient(...)` part runs the app's start-up, so the webhook
    sender runs in the background during the test.
    """
    numbers = count(1)
    with ExitStack() as stack:

        def start(**changes: object) -> TestClient:
            db_path = str(tmp_path / f"mockpay-{next(numbers)}.db")
            settings = Settings(**{**fast_settings(db_path, receiver.url), **changes})
            return stack.enter_context(TestClient(create_app(settings)))

        yield start


@pytest.fixture
def client(make_client: Callable[..., TestClient]) -> TestClient:
    return make_client()
