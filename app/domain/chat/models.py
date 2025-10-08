from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field

class Chat(SQLModel, table=True):
    __tablename__ = "chat"
    id: Optional[int] = Field(default=None, primary_key=True)
