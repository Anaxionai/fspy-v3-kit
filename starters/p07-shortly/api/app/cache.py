"""Redis cache-aside for redirects (task 17).

Key: link:<code>    Value: the target URL only    Expiry: settings.cache_ttl_seconds
"""

from sqlalchemy.ext.asyncio import AsyncSession

# TODO(task 17): create one shared async client here, with Redis from redis.asyncio:
#   Redis.from_url(settings.redis_url, decode_responses=True)
#   PATCH /links/{code} uses the same client to delete link:<code>.


async def get_target(code: str, session: AsyncSession) -> str | None:
    """Return the target URL for `code`, or None when the code does not exist.

    Input: the code, and the request's database session (from Depends(get_session)).
    Output: the target URL, or None for an unknown code (GET /{code} then answers 404).

    Must do (cache-aside): read link:<code> from Redis first; on a miss, read
    PostgreSQL and store the target with an expiry taken from settings.

    Edge cases the review checks:
    - An unknown code returns None and is not cached.
    - settings.cache_enabled is false: do not use Redis at all.
    - Redis raises redis.exceptions.RedisError: log a warning and read PostgreSQL,
      so a cache outage slows redirects down instead of breaking them.
    """
    raise NotImplementedError("TODO(task 17): cache-aside read of link:<code>")
