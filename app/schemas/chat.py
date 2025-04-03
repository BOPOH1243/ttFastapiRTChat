from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ChatType(str, Enum):
    private = "private"
    group = "group"

class ChatBase(BaseModel):
    title: Optional[str] = None
    type: ChatType

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    
    class Config:
        from_attributes = True