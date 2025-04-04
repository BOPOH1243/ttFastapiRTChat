# File: app/models/chat.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ChatType(str, enum.Enum):
    PRIVATE = "private"
    GROUP = "group"

# Ассоциативная таблица для участников чата
chat_users = Table(
    'chat_users',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    type = Column(Enum(ChatType), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Только для групповых чатов
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Участники (работает для всех типов)
    participants = relationship("User", secondary=chat_users, backref="chats")
    messages = relationship("Message", back_populates="chat")

    @property
    def is_group(self):
        return self.type == ChatType.GROUP