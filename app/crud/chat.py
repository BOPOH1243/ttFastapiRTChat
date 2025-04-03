from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat import Chat

class CRUDChat:
    async def create(self, db: AsyncSession, chat_data) -> Chat:
        db_chat = Chat(**chat_data.dict())
        db.add(db_chat)
        await db.commit()
        await db.refresh(db_chat)
        return db_chat

    async def get(self, db: AsyncSession, chat_id: int) -> Chat | None:
        result = await db.execute(select(Chat).filter(Chat.id == chat_id))
        return result.scalars().first()

crud_chat = CRUDChat()