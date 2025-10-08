from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel

class UserBase(SQLModel):
    pass  # añade campos compartidos aquí

class UserCreate(UserBase):
    pass  # campos requeridos para crear

class UserRead(UserBase):
    id: int

class UserPage(SQLModel):
    total: int
    items: List[UserRead]
