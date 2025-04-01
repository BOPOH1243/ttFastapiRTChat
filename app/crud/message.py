# File: app/crud/message.py
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message
from app.schemas.message import MessageCreate

async def create_message(db: AsyncSession, message: MessageCreate) -> Message | None:
    # Генерируем уникальный ID для предотвращения дублирования
    message_id = str(uuid.uuid4())
    db_message = Message(id=message_id, chat_id=message.chat_id, sender_id=message.sender_id, text=message.text)
    db.add(db_message)
    try:
        await db.commit()
        await db.refresh(db_message)
        return db_message
    except IntegrityError:
        await db.rollback()
        # Обработка дублирования сообщения
        return None

async def get_messages(db: AsyncSession, chat_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
    result = await db.execute(
        select(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).limit(limit).offset(offset)
    )
    return result.scalars().all()

async def mark_message_as_read(db: AsyncSession, message_id: str) -> Message | None:
    result = await db.execute(select(Message).filter(Message.id == message_id))
    db_message = result.scalars().first()
    if db_message:
        db_message.is_read = True
        await db.commit()
        await db.refresh(db_message)
    return db_message
