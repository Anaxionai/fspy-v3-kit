"""Tests for the token bucket in app/ratelimit.py (task 18).

conftest.py sets the burst to 5 and the rate to 10 a minute (one token every 6 seconds).
"""

import pytest
from httpx import AsyncClient
from redis.asyncio import Redis

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 18)")
async def test_burst_passes_then_the_next_call_fails(fresh_redis: Redis) -> None:
    """At now=1000.0, take_token(ip, now) passes five times and fails the sixth time."""
    raise NotImplementedError("TODO(task 18): write this test")


@pytest.mark.skip(reason="TODO(task 18)")
async def test_bucket_refills_with_time(fresh_redis: Redis) -> None:
    """After the sixth call fails at now=1000.0, a call at now=1006.0 passes."""
    raise NotImplementedError("TODO(task 18): write this test")


@pytest.mark.skip(reason="TODO(task 18)")
async def test_sixth_quick_post_gets_429(client: AsyncClient) -> None:
    """Six quick POST /links: five 201s, then 429 with a Retry-After header."""
    raise NotImplementedError("TODO(task 18): write this test")
