from __future__ import annotations
from logging.config import fileConfig
from importlib import import_module
from src.settings import settings

from alembic import context
from sqlalchemy import create_engine, pool
from sqlmodel import SQLModel


# Need to import models so metadata is populated
import_module("src.models")  # apps/api/src/models.py

# this is the Alembic Config object, which lets us access the values within .ini
config = context.config

# Override sqlalchemy.url from settings (should be consistent)
if settings.DATABASE_URL:
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging (set up loggers)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add the model's MetaData object here for 'autogenerate' support
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, but an Engine is also acceptable.
    By skipping the Engine creation we don't need an available DBAPI

    Calls to context.execute() here emit the given string to the script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine + associate a connection with the context

    """
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
