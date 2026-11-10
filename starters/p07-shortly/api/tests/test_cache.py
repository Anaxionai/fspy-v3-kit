"""Tests for the redirect cache in app/cache.py (task 17).

They use Redis database 1: the fresh_redis fixture empties it first, and you can
read keys with it, such as `await fresh_redis.ttl(f"link:{code}")`.
"""

import pytest
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 17)")
async def test_first_redirect_fills_the_cache(client: AsyncClient, fresh_redis: Redis) -> None:
    """Create a link and follow it once: link:<code> now holds the target, with a TTL above 0."""
    raise NotImplementedError("TODO(task 17): write this test")


@pytest.mark.skip(reason="TODO(task 17)")
async def test_cache_hit_serves_the_old_target(
    client: AsyncClient, fresh_redis: Redis, db: AsyncSession
) -> None:
    """Follow a link, change its target_url with plain SQL through `db`, then follow it again.

    The old, cached target comes back: the second redirect did not read PostgreSQL.
    """
    raise NotImplementedError("TODO(task 17): write this test")


@pytest.mark.skip(reason="TODO(task 17)")
async def test_patch_deletes_the_cached_key(client: AsyncClient, fresh_redis: Redis) -> None:
    """Follow a link, then PATCH it with X-Admin-Token (conftest.py sets ADMIN_TOKEN to "test-admin-token").

    link:<code> is gone, and the next redirect returns the new target.
    A PATCH with a wrong or missing token gets 403.
    """
    raise NotImplementedError("TODO(task 17): write this test")
