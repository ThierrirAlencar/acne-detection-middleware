# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. importa sua Base e TODOS os models (para o Alembic detectá-los)
from app.core.database import Base
from app.models.user import User  # repita para cada model

config = context.config
fileConfig(config.config_file_name)

# 2. aponta para o metadata dos seus models
target_metadata = Base.metadata

# 3. (opcional) sobrescreve a URL via variável de ambiente
import os
from dotenv import load_dotenv

load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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