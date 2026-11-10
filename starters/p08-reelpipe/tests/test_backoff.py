"""Tests for backoff_seconds() in worker/worker.py (task 12). They need no emulator.

When you have written the test, delete its @pytest.mark.skip line.
"""

import pytest

from worker import backoff_seconds  # noqa: F401 (your test uses it once you remove the skip)


@pytest.mark.skip(reason="TODO(task 12)")
def test_backoff_seconds():
    """Attempts 1, 2 and 3 wait 10, 20 and 40 seconds, and attempt 10 waits no more than 300.

    pytest.mark.parametrize (you met it in P1) checks all four attempts in one short test.
    """
    raise NotImplementedError("TODO(task 12): write this test, then delete the skip line")
