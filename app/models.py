from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    conversation_id = Column(Integer, index=True)
    created_at = Column(DateTime, index=True)
    summarized = Column(String)
    description = Column(String, index=True)
    # One-to-many relationship with messages
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation = relationship("Conversation", back_populates="message")
    content = Column(String, index=True)
    created_at = Column(DateTime, index=True)