"""The database connection: one async engine, and one session per request."""

import os
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# The cloud lab's PostgreSQL. Set DATABASE_URL to use another database,
# for example railseat_test in task 12.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://railseat:railseat@localhost:5432/railseat",
)

engine = create_async_engine(DATABASE_URL)

# expire_on_commit=False keeps an object's values readable after a commit,
# so the async session does not try to load them again.
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Give a route one session, and close it when the request ends.

    Routes get it with `session: AsyncSession = Depends(get_session)`.
    The tests swap it for a session on the test database.
    """
    async with SessionLocal() as session:
        yield session
