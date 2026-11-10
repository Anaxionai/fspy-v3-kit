"""Tests for video_ids() in lambda/handler.py (task 18). They need no emulator.

When you have written a test, delete its @pytest.mark.skip line.
"""

import json
from pathlib import Path

import pytest
from handler import video_ids  # noqa: F401 (your test uses it once you remove the skip)

EVENT_FILE = Path(__file__).resolve().parent.parent / "lambda" / "test-event.json"


@pytest.fixture
def event() -> dict:
    """The S3 ObjectCreated:Put event in lambda/test-event.json, read fresh for each test."""
    return json.loads(EVENT_FILE.read_text(encoding="utf-8"))


@pytest.mark.skip(reason="TODO(task 18)")
def test_video_ids_reads_the_upload(event):
    """video_ids(event) returns the id from the uploads/ key in test-event.json."""
    raise NotImplementedError("TODO(task 18): write this test, then delete the skip line")


@pytest.mark.skip(reason="TODO(task 18)")
def test_video_ids_ignores_keys_outside_uploads(event):
    """Change the record's key to one outside uploads/, such as status/<id>.json: video_ids returns []."""
    raise NotImplementedError("TODO(task 18): write this test, then delete the skip line")
