from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel

class ChatBase(SQLModel):
    pass  # añade campos compartidos aquí

class ChatCreate(ChatBase):
    pass  # campos requeridos para crear

class ChatRead(ChatBase):
    id: int

class ChatPage(SQLModel):
    total: int
    items: List[ChatRead]
