# File: app/schemas/message.py
from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    chat_id: int
    sender_id: int
    text: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True
