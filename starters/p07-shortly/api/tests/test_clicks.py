"""Tests for click counting in the worker (task 19).

Import the task with `from worker.tasks import count_click`. conftest.py sets
DATABASE_URL and REDIS_URL before that import, so count_click writes to the test database.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 19)")
async def test_redirect_sends_one_job_and_leaves_clicks(
    client: AsyncClient, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replace send_click with a fake that records its calls, using monkeypatch.setattr
    on the module where GET /{code} looks it up.

    Follow a link once: the fake was called once with the code, and clicks is still 0.
    """
    raise NotImplementedError("TODO(task 19): write this test")


@pytest.mark.skip(reason="TODO(task 19)")
async def test_count_click_adds_one(client: AsyncClient, db: AsyncSession) -> None:
    """Create a link, then call count_click(code, time.time()) directly (no worker needed).

    clicks for that link goes up by 1.
    """
    raise NotImplementedError("TODO(task 19): write this test")
