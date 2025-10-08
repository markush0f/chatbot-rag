from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from app.domain.


class Message(SQLModel, table=True):
    """Represents an individual message within a chat session."""

    __tablename__ = "message"

    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(
        foreign_key="chat.id",
        nullable=False,
        description="Reference to the parent chat session",
    )
    sender: str = Field(
        nullable=False, description="Indicates the sender (user or bot)"
    )
    content: str = Field(nullable=False, description="Text content of the message")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when the message was created",
    )

    # Relationship back to Chat
    chat: Optional[Chat] = Relationship(back_populates="messages")
