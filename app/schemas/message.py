from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    text: str
    chat_id: int
    sender_id: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime
    is_read: bool = False
    
    class Config:
        from_attributes = True