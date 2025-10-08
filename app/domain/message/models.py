from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    __tablename__ = "message"
    id: Optional[int] = Field(default=None, primary_key=True)
