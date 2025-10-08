from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel

class MessageBase(SQLModel):
    pass  # añade campos compartidos aquí

class MessageCreate(MessageBase):
    pass  # campos requeridos para crear

class MessageRead(MessageBase):
    id: int

class MessagePage(SQLModel):
    total: int
    items: List[MessageRead]
