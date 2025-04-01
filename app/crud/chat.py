# File: app/crud/chat.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chat import Chat
from app.schemas.chat import ChatBase

async def create_chat(db: AsyncSession, chat: ChatBase) -> Chat:
    db_chat = Chat(title=chat.title, type=chat.type)
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat

async def get_chat(db: AsyncSession, chat_id: int) -> Chat | None:
    result = await db.execute(select(Chat).filter(Chat.id == chat_id))
    return result.scalars().first()
