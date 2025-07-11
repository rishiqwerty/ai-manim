from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    created_at = Column(DateTime, index=True)
    summarized = Column(String)
    description = Column(String)
    # One-to-many relationship with messages
    messages = relationship("Message", back_populates="conversation")

class MessageType(Enum):
    user = "user"
    assistant = "assistant"
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation = relationship("Conversation", back_populates="message")
    message_type = Column(SQLAlchemyEnum(MessageType), nullable=False)
    content = Column(String)
    created_at = Column(DateTime, index=True)