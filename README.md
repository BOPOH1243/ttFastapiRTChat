# Real-Time Chat Application

## Описание

Это чатовое приложение с поддержкой обмена сообщениями в реальном времени.  
**Основные возможности**:
- Обмен сообщениями через REST API
- Мгновенные уведомления о новых событиях через WebSocket
- JWT-аутентификация для всех операций
- Автоматическая документация API (Swagger/OpenAPI)

## Технологии
- Python (FastAPI)
- WebSocket
- PostgreSQL (основная БД)
- Docker/Docker-compose
- JWT-токены

## Установка и запуск

1. Склонируйте репозиторий:
```bash
git clone https://github.com/BOPOH1243/ttFastapiRTChat.git
cd ttFastapiRTChat
```

2. Запустите через Docker:
```bash
sudo docker-compose up -d
```

Приложение будет доступно на `http://localhost` или `http://localhost:8000` если не пробрасывать nginx

## Документация API
После запуска откройте в браузере:  
`http://localhost/docs`  
Полное описание всех REST-эндпоинтов и схем данных доступно в интерактивной документации.

## Работа с WebSocket

Для получения уведомлений подключитесь к:
```
ws://localhost:8000/ws/notif?token=<JWT_TOKEN>
```

**Формат событий**:
```json
{
  "type": "тип_события",
  "payload": { ... данные события ... }
}
```

Примеры событий:
- `new_message` - новое сообщение в чате
- `update_chat` - изменения в чате
- `create_chat` - создание чата с пользователем

## Особенности реализации
1. **Авторизация**:  
   Все эндпоинты (включая WebSocket) требуют JWT-токен в query-параметре `token`.

2. **Уведомления**:  
   WebSocket-канал отправляет события только для:
   - Чатов, где пользователь является участником
   - Изменений, касающихся текущего пользователя

3. **Масштабирование**:  
   Готово к развёртыванию в Docker-окружении с поддержкой горизонтального масштабирования.

## Пример использования
Подключение через WebSocket (using `wscat`):
```bash
wscat -c "ws://localhost:8000/ws/notif?token=ваш.jwt.токен"
```

При новом сообщении в чате получите:
```json
{
  "type": "new_message",
  "payload": {
    "id": 42,
    "text": "Привет из чата!",
    "chat_id": 1,
    "sender_id": 2,
    "created_at": "2024-02-20T15:30:00Z"
  }
}
```