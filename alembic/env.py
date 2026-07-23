import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# 프로젝트 루트를 sys.path에 추가하여 app 모듈을 임포트할 수 있게 함
import os
import sys
sys.path.append(os.getcwd())

from app.core.db.databases import Base

# Model Import
from app import models

# Alembic Config object
config = context.config

# 환경 변수에서 DB_HOST를 가져오되, 없으면 기본값으로 'localhost' 사용
db_host = os.getenv("DB_HOST", "mysql")
URL_STR = f"mysql+asyncmy://root:1234@{db_host}:3306/oz_database"
config.set_main_option("sqlalchemy.url", URL_STR)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# model's MetaData object
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    # URL을 직접 가져와서 create_async_engine을 사용합니다.
    url = config.get_main_option("sqlalchemy.url")
    
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
