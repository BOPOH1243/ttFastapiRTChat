from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.chat_service import manager

router = APIRouter(tags=['websocket'])


@router.websocket("/ws/notif")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket-эндпоинт для уведомлений.
    
    Клиент должен подключаться по URL: /ws/notif?token=<jwt token>
    После валидации токена соединение сохраняется, и далее сервер может отправлять уведомления
    данному пользователю по его ID через функцию manager.send_notification().
    
    Цикл while поддерживает соединение активным.
    """
    user_id = None
    try:
        # Извлекаем токен и валидируем его внутри менеджера.
        user_id = await manager.connect(websocket)
        while True:
            # Ожидаем входящих сообщений от клиента (например, ping)
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Клиент отключился, удаляем соединение.
        if user_id is not None:
            manager.disconnect(user_id)
    except Exception:
        # При возникновении любой ошибки, также отключаем соединение.
        if user_id is not None:
            manager.disconnect(user_id)
