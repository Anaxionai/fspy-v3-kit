"""The race test for is_new_point (task 9).

Start Redis and the API first (uv run fastapi dev api/app/main.py). This test calls that API
through the `live_client` fixture in conftest.py.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 9)")
async def test_one_point_sent_20_times_at_once_is_accepted_once(live_client):
    """Post one point for rider 900, with seq=int(time.time() * 1000), 20 times at the same
    moment (asyncio.gather). Exactly one answer may say "accepted": true.

    It should fail with the simple is_new_point and pass after your atomic fix.
    """
    raise NotImplementedError("TODO(task 9): send the same point 20 times at once")
