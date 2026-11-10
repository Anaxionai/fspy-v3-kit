"""Shared test set-up: a test database, a test client and test data.

The tests never touch your `railseat` database. They use `railseat_test`,
which you make once (task 12, "Before you start"):

    docker exec cloudlab-postgres-1 createdb -U railseat railseat_test

and fill with your tables (task 12, step 2):

    DATABASE_URL=postgresql+asyncpg://railseat:railseat@localhost:5432/railseat_test uv run alembic upgrade head
"""

import os
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db import get_session
from app.main import app

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://railseat:railseat@localhost:5432/railseat_test",
)

# NullPool: every session opens its own connection and closes it after use.
# Each test runs in its own event loop, and a connection kept in a pool from
# an earlier loop fails with "attached to a different loop".
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestSession = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture
def anyio_backend() -> str:
    """Run the async tests (marked @pytest.mark.anyio) on asyncio, not trio."""
    return "asyncio"


async def get_test_session() -> AsyncIterator[AsyncSession]:
    """Give each request its own session on the test database."""
    async with TestSession() as session:
        yield session


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """An HTTP client that calls the app in memory, on the test database.

    Use it in a test like this: `response = await client.post("/bookings", json=...)`.
    """
    app.dependency_overrides[get_session] = get_test_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
async def one_seat() -> AsyncIterator[dict[str, int]]:
    """Known data for a booking test: one train, coach, seat and journey.

    TODO(task 12):
    - Empty the tables first, with one `TRUNCATE ... RESTART IDENTITY CASCADE`
      of all eight tables, in a session from TestSession.
    - Add one train, one coach, one seat and one journey, plus any rows they
      point to (such as stations), and commit.
    - `yield {"journey_id": ..., "seat_id": ...}` so a test can book that seat.
    - After the yield, empty the tables again, so a failed run leaves no
      double bookings behind.
    """
    raise NotImplementedError("TODO(task 12): create one bookable seat, then clean up")
