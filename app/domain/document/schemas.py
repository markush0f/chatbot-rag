
from typing import Optional, List
from sqlmodel import SQLModel

class DocumentBase(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None

class DocumentCreate(DocumentBase):
    name: str

class DocumentRead(DocumentBase):
    id: int
    name: str

class DocumentUpdate(DocumentBase):
    pass

class DocumentPage(SQLModel):
    total: int
    items: List[DocumentRead]
