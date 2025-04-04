from pydantic import BaseModel
from typing import List, Optional
from app.models.chat import ChatType  # Предполагается, что ChatType определён в модели

class ChatBase(BaseModel):
    """
    Базовая схема чата.
    """
    title: Optional[str] = None
    type: ChatType


class ChatCreate(ChatBase):
    """
    Схема для создания нового чата.
    
    Поле `participant_ids` содержит список идентификаторов пользователей,
    которые будут участниками чата.
    Поле `creator_id` не передаётся клиентом, а берётся из токена.
    """
    participant_ids: Optional[List[int]] = []


class ChatUpdate(BaseModel):
    """
    Схема для обновления чата.
    
    Позволяет обновлять заголовок, состояние активности и участников чата.
    """
    title: Optional[str] = None
    is_active: Optional[bool] = None
    participant_ids: Optional[List[int]] = None


class Chat(ChatBase):
    """
    Схема для ответа с данными чата.
    
    Поля:
      - id: идентификатор чата;
      - creator_id: идентификатор создателя (из токена);
      - is_active: состояние активности чата;
      - participant_ids: список идентификаторов участников.
    """
    id: int
    creator_id: Optional[int]
    is_active: bool
    participant_ids: List[int] = []

    class Config:
        orm_mode = True
        from_attributes=True
