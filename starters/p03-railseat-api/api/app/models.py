"""RailSeat's tables as SQLAlchemy models.

Alembic reads `Base.metadata` (see alembic/env.py) to write your migrations,
so every model must inherit from `Base`.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """The parent class of every RailSeat model."""


# TODO(task 9): write the eight models from your docs/erd.md here:
#   Station, Train, Stop, Coach, Seat, Journey, Passenger and Booking.
#   - Use the SQLAlchemy 2.0 style: `Mapped[...]` and `mapped_column(...)`.
#   - Give each model a `__tablename__`, such as "bookings". Your loader and
#     your test fixture empty the tables by these names.
#   - Every foreign key in your ERD becomes `ForeignKey("table.column")`.
#   - Every uniqueness rule in your ERD except the booking rule becomes a
#     constraint, such as `__table_args__ = (UniqueConstraint("train_id", "code"),)`.
#   - Booking needs a `status` column: "confirmed" or "cancelled".
#   - `relationship()` is optional. The async session cannot load one later,
#     so join the tables in your queries instead.
#
# TODO(task 12): add the partial unique index from step 8 of task 12 to
#   Booking's `__table_args__`: at most one confirmed booking per seat per
#   journey. Then autogenerate a migration and read it before you upgrade.
