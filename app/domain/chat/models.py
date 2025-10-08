from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Chat(SQLModel, table=True):
    """Represents a chat session between a user and the chatbot."""

    __tablename__ = "chat"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(
        default=None, description="Title or summary of the chat session"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when the chat was created",
    )

    # One-to-many relationship with Message
    messages: List["Message"] = Relationship(back_populates="chat")
