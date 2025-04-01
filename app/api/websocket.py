# File: app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.chat_service import manager
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.message import create_message
from app.schemas.message import MessageCreate

router = APIRouter()

@router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Сохраняем сообщение в БД с использованием уникального идентификатора
            message_data = MessageCreate(chat_id=chat_id, sender_id=user_id, text=data)
            created_message = await create_message(db, message_data)
            if created_message:
                # Рассылка сообщения всем подключённым клиентам
                await manager.broadcast(f"User {user_id} in Chat {chat_id}: {data}")
            else:
                # Уведомление о дублировании или ошибке
                await manager.send_personal_message("Duplicate message detected", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {user_id} disconnected from Chat {chat_id}")
