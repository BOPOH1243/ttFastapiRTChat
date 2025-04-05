#!/bin/bash
set -e

# Ждем, пока PostgreSQL не станет доступен
until nc -z db 5432; do
  echo "Ожидание запуска БД..."
  sleep 1
done

export PYTHONPATH=$(pwd)
# Применяем миграции через Alembic
alembic upgrade head

# Запускаем приложение (например, внутри app/main.py уже вызывается uvicorn)
python app/main.py
