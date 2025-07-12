from enum import Enum
from sqlalchemy import Column, JSON, Integer, String, DateTime, Enum as SQLAlchemyEnum, ForeignKey
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
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    conversation = relationship("Conversation", back_populates="messages")
    message_type = Column(SQLAlchemyEnum(MessageType), nullable=False)
    content = Column(String)
    created_at = Column(DateTime, index=True)

class JobStatus(Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
class Job(Base):
    """Stores information of a manim video generation."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"),index=True)
    status = Column(SQLAlchemyEnum(JobStatus), default=JobStatus.pending, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    video_path = Column(String, nullable=True)
    logs = Column(JSON, nullable=True)
