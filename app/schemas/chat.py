# File: app/schemas/chat.py
from pydantic import BaseModel
from enum import Enum

class ChatType(str, Enum):
    private = "private"
    group = "group"

class ChatBase(BaseModel):
    title: str | None = None
    type: ChatType

class ChatResponse(ChatBase):
    id: int

    class Config:
        orm_mode = True
