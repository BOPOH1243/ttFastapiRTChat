# File: migrations/env.py
import os
import sys
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

# Добавляем путь к проекту, чтобы можно было импортировать модули
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Импортируем настройки и базовый класс моделей
from app.core.config import settings
from app.core.database import engine, Base

# Импорт всех моделей, чтобы Alembic "видел" метаданные
import app.models.user
import app.models.chat
import app.models.group
import app.models.message

# Настройка логирования из alembic.ini
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в режиме offline."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в режиме online с использованием асинхронного движка."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
