import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user import User  # Импорт модели пользователя для вложенного представления
from typing import List

class MessageBase(BaseModel):
    """
    Базовая схема для сообщения.
    """
    text: str
    chat_id: int
    sender_id: int  # Будет переопределён в API эндпоинте из токена

class MessageCreate(MessageBase):
    """
    Схема для создания сообщения.
    Используется клиентом при отправке нового сообщения.
    """
    pass

class Message(MessageBase):
    """
    Схема для ответа с данными сообщения.
    Генерирует уникальный UUID по умолчанию.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime
    is_read: bool = False

    class Config:
        orm_mode = True  # Позволяет Pydantic работать с ORM объектами

class MessageResponse(BaseModel):
    """
    Схема для детального представления сообщения, включая данные отправителя.
    """
    id: str
    text: str
    sender: User  # Представление отправителя как объекта User
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True
        from_attributes=True


class MessageListResponse(BaseModel):
    """
    Схема для ответа с массивом сообщений.
    """
    messages: List[MessageResponse]
    total: int  # Общее количество сообщений в чате

    class Config:
        orm_mode = True
