FROM python:3.10-slim

WORKDIR /app

# Установка системных зависимостей (если нужно)
RUN apt-get update && apt-get install -y netcat-openbsd gcc build-essential

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем всё приложение в контейнер
COPY . .

# Делаем скрипт запуска исполняемым
RUN chmod +x ./entrypoint.sh

# Запускаем скрипт входа
CMD ["./entrypoint.sh"]
