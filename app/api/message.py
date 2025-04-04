from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.message import MessageCreate, Message, MessageListResponse, MessageResponse
from app.crud.message import crud_message
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User as UserModel
router = APIRouter(prefix="/message", tags=["message"])

@router.post("/", response_model=Message, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_create: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    API эндпоинт для отправки сообщения в чат.
    
    Данные:
      - **text**: Текст сообщения.
      - **chat_id**: Идентификатор чата, в который отправляется сообщение.
      
    Идентификатор отправителя (sender_id) берётся из токена текущего пользователя.
    """
    # Переопределяем sender_id, чтобы предотвратить подделку от клиента
    message_data = message_create.dict()
    message_data["sender_id"] = current_user.id

    new_message = await crud_message.create(db, message_data)
    return new_message

@router.get("/chat/{chat_id}/", response_model=MessageListResponse)
async def get_chat_messages(
    chat_id: int,
    offset: int = Query(0, ge=0, description="Смещение (количество пропускаемых сообщений)"),
    limit: int = Query(20, le=100, description="Максимальное количество сообщений за запрос (не более 100)"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Получает все сообщения из чата с поддержкой пагинации.

    - **chat_id**: ID чата, из которого получаем сообщения.
    - **offset**: Количество сообщений, которые нужно пропустить (по умолчанию 0).
    - **limit**: Количество сообщений на странице (по умолчанию 20, максимум 100).

    Возвращает массив сообщений и общее количество сообщений в чате.
    """
    messages, total = await crud_message.get_by_chat_paginated(db, chat_id, offset, limit)

    # ✅ Преобразуем объекты SQLAlchemy в Pydantic-модели
    messages_pydantic = [
        MessageResponse(
            id=msg.id,
            text=msg.text,
            sender=msg.sender,  # Убедись, что sender - это объект, который можно сериализовать
            timestamp=msg.timestamp.isoformat(),
            is_read=msg.is_read
        )
        for msg in messages
    ]

    return MessageListResponse(messages=messages_pydantic, total=total)

