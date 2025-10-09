from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.domain.user.models import User


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
    
    user_id: int = Field(
        foreign_key="user.id",
        nullable=False,
        description="Reference to the user who owns this chat",
    )
    user: User | None = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")
