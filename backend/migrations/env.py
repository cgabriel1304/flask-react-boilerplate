"""Generic single-database configuration."""
from __future__ import with_statement

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from db import db
from config import config as app_config
import os

# this is the Alembic Config object, which provides
# the values of the alembic.ini file, plus other values that can be
# passed programmatically to script_context.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a SQLALCHEMY_DATABASE_URI
    setting to be present for
    the application's models with an in-memory SQLite database
    to be available for offline use.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    configuration = app_config[os.getenv('FLASK_ENV', 'development')]
    url = configuration.SQLALCHEMY_DATABASE_URI

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = app_config[os.getenv('FLASK_ENV', 'development')]
    
    engine = engine_from_config(
        {'sqlalchemy.url': configuration.SQLALCHEMY_DATABASE_URI},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
