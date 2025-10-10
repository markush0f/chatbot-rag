
from typing import List, Optional, Any
from sqlmodel import Session
from .models import Document
from .repository import DocumentRepository
from .schemas import DocumentCreate, DocumentUpdate

class DocumentService:
    def __init__(self, session: Session):
        self.repo = DocumentRepository(session)

    def list_with_total(
        self, offset: int, limit: int, filters: dict[str, Any] | None = None
    ) -> tuple[list[Document], int]:
        items_seq = self.repo.list_with_filters(offset=offset, limit=limit, filters=filters)
        items: List[Document] = list(items_seq)
        total = self.repo.count()
        return items, total

    def get(self, id: int) -> Optional[Document]:
        return self.repo.get(id)

    def create(self, data: DocumentCreate) -> Document:
        obj = Document.model_validate(data.model_dump())
        return self.repo.create(obj)

    def update(self, id: int, data: DocumentUpdate) -> Optional[Document]:
        obj = self.repo.get(id)
        if not obj:
            return None
        return self.repo.update(obj, data.model_dump(exclude_unset=True))

    def delete(self, id: int) -> bool:
        obj = self.repo.get(id)
        if not obj:
            return False
        self.repo.delete(obj)
        return True
