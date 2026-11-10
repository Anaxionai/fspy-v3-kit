"""Create the four seed users for local work and tests (P5 add-on, task 11, step 7).

Run it from railseat/api after `uv run alembic upgrade head`:

    uv run python -m seed.make_users

The password comes from SEED_PASSWORD in api/.env. It is never written in code.
Running it twice is safe: existing users are updated, not duplicated.
"""

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.db import SessionLocal
from app.security import hash_password

# Emails use @example.com: Pydantic's EmailStr refuses .test and .local addresses.
USERS = [
    ("asha@example.com", "passenger"),
    ("ravi@example.com", "passenger"),
    ("agent@example.com", "agent"),
    ("admin@example.com", "admin"),
]


async def save_user(
    session: AsyncSession, email: str, role_name: str, password_hash: str
) -> None:
    """Insert this user, or update the user with this email if one exists.

    The user ends up verified (`is_verified` true), with the role named
    `role_name` (look the Role row up by name) and this password hash.
    Do not commit here; main() commits once.
    """
    raise NotImplementedError("TODO(task 11): insert or update one seed user")


async def main() -> None:
    if len(settings.SEED_PASSWORD) < 10:
        raise SystemExit("Set SEED_PASSWORD in api/.env first: 10 or more characters.")
    async with SessionLocal() as session:
        for email, role_name in USERS:
            await save_user(
                session, email, role_name, hash_password(settings.SEED_PASSWORD)
            )
        await session.commit()
    print(f"Seeded {len(USERS)} users: " + ", ".join(email for email, _ in USERS))


if __name__ == "__main__":
    asyncio.run(main())
