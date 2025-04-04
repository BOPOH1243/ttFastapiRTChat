from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.message import Message as MessageModel

class CRUDMessage:
    """
    CRUD-операции для модели Message.
    """

    async def create(self, db: AsyncSession, message_data: dict) -> MessageModel:
        """
        Создаёт новое сообщение.
        
        :param db: Асинхронная сессия базы данных.
        :param message_data: Словарь с данными сообщения.
        :return: Созданное сообщение.
        """
        new_message = MessageModel(**message_data)
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return new_message

    async def get(self, db: AsyncSession, message_id: str) -> Optional[MessageModel]:
        """
        Получает сообщение по идентификатору.
        
        :param db: Асинхронная сессия базы данных.
        :param message_id: Идентификатор сообщения.
        :return: Объект Message или None.
        """
        result = await db.execute(select(MessageModel).filter(MessageModel.id == message_id))
        return result.scalars().first()

    async def get_by_chat(self, db: AsyncSession, chat_id: int, skip: int = 0, limit: int = 100) -> List[MessageModel]:
        """
        Получает список сообщений для конкретного чата.
        
        :param db: Асинхронная сессия базы данных.
        :param chat_id: Идентификатор чата.
        :param skip: Количество пропускаемых записей для пагинации.
        :param limit: Максимальное число записей.
        :return: Список сообщений.
        """
        result = await db.execute(
            select(MessageModel).filter(MessageModel.chat_id == chat_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_chat_paginated(self, db: AsyncSession, chat_id: int, offset: int = 0, limit: int = 20):
        """
        Получает список сообщений в чате с поддержкой пагинации.
        
        :param db: Асинхронная сессия базы данных.
        :param chat_id: Идентификатор чата.
        :param offset: Количество пропускаемых записей (по умолчанию 0).
        :param limit: Максимальное количество сообщений (по умолчанию 20).
        :return: Список сообщений и общее количество сообщений в чате.
        """
        query = select(MessageModel).filter(MessageModel.chat_id == chat_id).offset(offset).limit(limit)
        messages_result = await db.execute(query)
        messages = messages_result.scalars().all()

        # Получаем общее количество сообщений в чате
        total_result = await db.execute(select(func.count()).filter(MessageModel.chat_id == chat_id))
        total_messages = total_result.scalar()

        return messages, total_messages
    async def update(self, db: AsyncSession, db_message: MessageModel, update_data: dict) -> MessageModel:
        """
        Обновляет сообщение.
        
        :param db: Асинхронная сессия базы данных.
        :param db_message: Объект сообщения для обновления.
        :param update_data: Словарь с обновлёнными данными.
        :return: Обновлённое сообщение.
        """
        for key, value in update_data.items():
            setattr(db_message, key, value)
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        return db_message

    async def remove(self, db: AsyncSession, db_message: MessageModel) -> MessageModel:
        """
        Удаляет сообщение.
        
        :param db: Асинхронная сессия базы данных.
        :param db_message: Объект сообщения для удаления.
        :return: Удалённое сообщение.
        """
        await db.delete(db_message)
        await db.commit()
        return db_message

crud_message = CRUDMessage()
