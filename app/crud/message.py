from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message

class CRUDMessage:
    async def create(self, db: AsyncSession, message_data) -> Message:
        db_message = Message(**message_data.dict())
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        return db_message

    async def get_chat_messages(self, db: AsyncSession, chat_id: int, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Message)
            .filter(Message.chat_id == chat_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

crud_message = CRUDMessage()