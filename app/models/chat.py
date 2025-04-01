# File: app/models/chat.py
from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base
import enum

class ChatType(enum.Enum):
    private = "private"
    group = "group"

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    type = Column(Enum(ChatType), nullable=False)
