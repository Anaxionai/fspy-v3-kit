"""Tests for app/settings.py (task 10). Import Settings from app.settings when you write the test."""

import pytest


@pytest.mark.skip(reason="TODO(task 10)")
def test_settings_reads_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """monkeypatch.setenv("LOG_LEVEL", "debug"), then a new Settings() has log_level "debug"."""
    raise NotImplementedError("TODO(task 10): write this test")
