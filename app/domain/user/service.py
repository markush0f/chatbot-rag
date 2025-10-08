from typing import List
from sqlmodel import Session
from .models import User
from .repository import UserRepository
from .schemas import UserCreate

class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def list_with_total(self, offset: int, limit: int) -> tuple[list[User], int]:
        items_seq = self.repo.list(offset=offset, limit=limit)
        items: List[User] = list(items_seq)
        total = self.repo.count()
        return items, total

    def create(self, data: UserCreate) -> User:
        # CORREGIDO: convertir schema a dict
        obj = User.model_validate(data.model_dump())
        return self.repo.create(obj)
