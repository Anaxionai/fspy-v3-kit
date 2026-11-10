"""Tests for POST /uploads/{video_id}/complete (task 9).

They talk to Floci, so start it and run `bash aws/setup.sh` first. When you have written a
test, delete its @pytest.mark.skip line.
"""

import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.skip(reason="TODO(task 9)")
def test_complete_unknown_id_returns_404(client):
    """complete for a video_id with no object under uploads/ answers 404."""
    raise NotImplementedError("TODO(task 9): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 9)")
def test_complete_returns_202_and_sends_one_job(client):
    """Put a small object at uploads/<a new id> first. Then complete answers 202, and the
    queue's ApproximateNumberOfMessages is one more than before.
    """
    raise NotImplementedError("TODO(task 9): write this test, then delete the skip line")
