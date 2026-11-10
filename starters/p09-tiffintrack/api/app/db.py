"""The API's connections to Redis and MongoDB.

The lifespan in main.py opens them once when the API starts and closes them when it stops.
Every other file gets them with get_redis() and get_db().
"""

import redis.asyncio
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.settings import MONGO_DB, MONGO_URL, REDIS_URL

_redis: redis.asyncio.Redis | None = None
_mongo: AsyncMongoClient | None = None


async def open_connections() -> None:
    """Create one Redis client and one MongoDB client.

    Neither client connects until it is first used, so the API starts even when the
    cloud lab is stopped. A request that needs Redis or MongoDB fails until it runs.
    """
    global _redis, _mongo
    _redis = redis.asyncio.from_url(REDIS_URL, decode_responses=True)
    _mongo = AsyncMongoClient(MONGO_URL)


async def close_connections() -> None:
    """Close both clients when the API stops."""
    global _redis, _mongo
    if _redis is not None:
        await _redis.aclose()
    if _mongo is not None:
        await _mongo.close()
    _redis = None
    _mongo = None


def get_redis() -> redis.asyncio.Redis:
    """The API's one Redis client. With decode_responses=True, Redis gives back text, not bytes."""
    if _redis is None:
        raise RuntimeError("Redis is not open. The API's lifespan opens it at start-up.")
    return _redis


def get_db() -> AsyncDatabase:
    """The MongoDB database named by MONGO_DB: tiffintrack, or tiffintrack_test in the tests."""
    if _mongo is None:
        raise RuntimeError("MongoDB is not open. The API's lifespan opens it at start-up.")
    return _mongo[MONGO_DB]


async def create_indexes() -> None:
    """Create the indexes TiffinTrack needs. The lifespan runs this at every start-up.

    TODO(task 16): create these three indexes in get_db():
      - a 2dsphere index on points.location;
      - a 2dsphere index on riders.location (the nearest-rider query in task 19 needs it);
      - a unique index on points over (rider_id, seq), so MongoDB refuses an exact copy of a point.
    Creating an index that already exists does nothing, so this is safe at every start-up.
    Until task 16 this function does nothing, so the API can start without MongoDB.
    """
