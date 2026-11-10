"""Database tables for Shortly (SQLAlchemy 2.0 typed mappings)."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for every table. Alembic reads `Base.metadata` (see alembic/env.py)."""


class Link(Base):
    """One short link.

    Keep the table name `links` and the column name `code`: P11, P13 and the
    mentor's incident drill use them.
    """

    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO(task 7): add the other columns, then make the migration with Alembic:
    #   code        7 characters, with a unique index (the database refuses a duplicate code)
    #   target_url  the long URL, as text
    #   clicks      a whole number that starts at 0; give it a database-side default too,
    #               so a plain SQL INSERT (the k6 seed in task 20) can leave it out
    #   created_at  when the link was made, filled in by the database
