from typing import List
from sqlmodel import Session
from .models import Chat
from .repository import ChatRepository
from .schemas import ChatCreate

class ChatService:
    def __init__(self, session: Session):
        self.repo = ChatRepository(session)

    def list_with_total(self, offset: int, limit: int) -> tuple[list[Chat], int]:
        items_seq = self.repo.list(offset=offset, limit=limit)
        items: List[Chat] = list(items_seq)
        total = self.repo.count()
        return items, total

    def create(self, data: ChatCreate) -> Chat:
        obj = Chat.model_validate(data.model_dump())
        return self.repo.create(obj)

    def list_by_user(self, user_id: int) -> List[Chat]:
        """Get all chats from a user."""
        return self.repo.get_user_chats(user_id)