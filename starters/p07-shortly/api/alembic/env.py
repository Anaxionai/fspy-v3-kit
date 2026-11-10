"""Alembic's entry point: connects to PostgreSQL and runs the migrations.

Migrations use a plain (sync) connection. psycopg 3 serves both sync and async,
so the same DATABASE_URL works here and in the API.
"""

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# TODO(task 10): read the URL from settings.database_url (app/settings.py) instead of os.environ.
database_url = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://railseat:railseat@localhost:5432/shortly"
)
# The ini format treats % as special, so a % in a password must be doubled.
config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

# Alembic compares this with the database when you run `alembic revision --autogenerate`.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Print the SQL instead of running it (alembic upgrade head --sql)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Connect to the database and run the migrations."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
