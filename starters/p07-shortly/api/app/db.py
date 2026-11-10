"""Database connection for the API: async SQLAlchemy with psycopg 3, as in RailSeat.

psycopg works both async (this API) and sync (the Celery worker in task 19),
so the API and the worker share one driver and one URL format.
"""

import os
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# TODO(task 10): read the URL from settings.database_url (app/settings.py) instead of os.environ.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://railseat:railseat@localhost:5432/shortly"
)

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: one session per request.

    Routes get sessions only through `Depends(get_session)`, so the tests can swap
    in the test database (see tests/conftest.py).
    """
    async with SessionLocal() as session:
        yield session


# Write `session: SessionDep` in a route to get a session from get_session.
SessionDep = Annotated[AsyncSession, Depends(get_session)]
