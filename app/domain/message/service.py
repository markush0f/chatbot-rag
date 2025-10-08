from typing import List
from sqlmodel import Session
from .models import Message
from .repository import MessageRepository
from .schemas import MessageCreate

class MessageService:
    def __init__(self, session: Session):
        self.repo = MessageRepository(session)

    def list_with_total(self, offset: int, limit: int) -> tuple[list[Message], int]:
        items_seq = self.repo.list(offset=offset, limit=limit)
        items: List[Message] = list(items_seq)
        total = self.repo.count()
        return items, total

    def create(self, data: MessageCreate) -> Message:
        # CORREGIDO: convertir schema a dict
        obj = Message.model_validate(data.model_dump())
        return self.repo.create(obj)
