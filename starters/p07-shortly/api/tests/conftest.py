"""Test set-up for Shortly's API (RailSeat style). You do not need to change it.

The tests run on your laptop against the cloud lab:
- PostgreSQL database shortly_test (create it and migrate it once, see STARTER.md);
- Redis database 1, so the tests never touch the data in database 0.
In CI (P11), point them at the service containers with the variables
TEST_DATABASE_URL and TEST_REDIS_URL.
"""

import asyncio
import os
import sys
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+psycopg://railseat:railseat@localhost:5432/shortly_test"
)
TEST_REDIS_URL = os.environ.get("TEST_REDIS_URL", "redis://localhost:6379/1")

# The app reads its settings when it is imported, so set them before any test imports it.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["REDIS_URL"] = TEST_REDIS_URL
os.environ["ADMIN_TOKEN"] = "test-admin-token"  # a test value, not a secret
os.environ["PUBLIC_BASE_URL"] = "http://test"
os.environ["CACHE_ENABLED"] = "true"
os.environ["RATE_LIMIT_BURST"] = "5"
os.environ["RATE_LIMIT_PER_MINUTE"] = "10"

# NullPool: every session opens a new connection, so none is shared between tests.
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestSession = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def anyio_backend() -> object:
    """Run async tests on asyncio. On Windows, psycopg's async mode needs the selector loop."""
    if sys.platform == "win32":
        return ("asyncio", {"loop_factory": asyncio.SelectorEventLoop})
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def one_event_loop(anyio_backend: object) -> AsyncIterator[None]:
    """Keep one event loop for the whole run.

    Then the module-level Redis client you create in app/cache.py keeps working
    from one test to the next.
    """
    yield


async def _test_session() -> AsyncIterator[AsyncSession]:
    async with TestSession() as session:
        yield session


@pytest.fixture
async def db() -> AsyncIterator[AsyncSession]:
    """A session on the test database. The links table is emptied first."""
    async with TestSession() as session:
        await session.execute(text("TRUNCATE links RESTART IDENTITY"))
        await session.commit()
        yield session


@pytest.fixture
async def fresh_redis() -> AsyncIterator[Redis]:
    """A client on Redis database 1, emptied first. Use it to look at keys such as link:<code>."""
    client = Redis.from_url(TEST_REDIS_URL, decode_responses=True)
    await client.flushdb()
    yield client
    await client.aclose()


@pytest.fixture
async def client(db: AsyncSession, fresh_redis: Redis) -> AsyncIterator[AsyncClient]:
    """An HTTP client on the app, with an empty links table and an empty Redis database 1."""
    # Imported here, not at the top, so the variables above are set first.
    from app.db import get_session
    from app.main import app

    app.dependency_overrides[get_session] = _test_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http
    app.dependency_overrides.clear()
