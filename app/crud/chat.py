from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.chat import Chat, chat_users
from app.models.user import User

class CRUDChat:
    """Класс для операций CRUD над чатами."""

    async def get(self, db: AsyncSession, chat_id: int) -> Optional[Chat]:
        """
        Получает чат по идентификатору с предварительной загрузкой участников.
        """
        query = (
            select(Chat)
            .options(selectinload(Chat.participants))
            .filter(Chat.id == chat_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Chat]:
        """
        Получает список чатов с поддержкой пагинации и предварительной загрузкой участников.
        """
        query = (
            select(Chat)
            .options(selectinload(Chat.participants))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, chat_data: dict, current_user: User) -> Chat:
        """
        Создаёт новый чат.
        
        Поле `creator_id` берётся из токена (current_user).
        Если передан список идентификаторов участников (participant_ids), то они добавляются в чат.
        """
        new_chat = Chat(
            title=chat_data.get("title"),
            type=chat_data.get("type"),
            is_active=True,
            creator_id=current_user.id
        )
        # Если переданы идентификаторы участников, загружаем их из БД и связываем с чатом.
        if "participant_ids" in chat_data and chat_data["participant_ids"]:
            result = await db.execute(
                select(User).filter(User.id.in_(chat_data["participant_ids"]))
            )
            users = result.scalars().all()
            new_chat.participants = users

        db.add(new_chat)
        await db.commit()
        # Принудительно обновляем объект, чтобы избежать ленивой загрузки
        await db.refresh(new_chat, attribute_names=["participants"])
        return new_chat

    async def update(self, db: AsyncSession, db_chat: Chat, update_data: dict) -> Chat:
        """
        Обновляет данные чата.
        
        Если переданы новые идентификаторы участников (participant_ids),
        они заменяют текущий список участников.
        """
        # Обработка обновления обычных полей
        for key, value in update_data.items():
            if key != "participant_ids":
                setattr(db_chat, key, value)
        # Обработка поля participant_ids
        if "participant_ids" in update_data and update_data["participant_ids"] is not None:
            participant_ids = update_data["participant_ids"]
            result = await db.execute(select(User).filter(User.id.in_(participant_ids)))
            users = result.scalars().all()
            db_chat.participants = users

        db.add(db_chat)
        await db.commit()
        # Принудительно обновляем объект с участниками
        await db.refresh(db_chat, attribute_names=["participants"])
        return db_chat

    async def remove(self, db: AsyncSession, db_chat: Chat) -> Chat:
        """
        Удаляет чат из базы данных.
        """
        await db.delete(db_chat)
        await db.commit()
        return db_chat

crud_chat = CRUDChat()
