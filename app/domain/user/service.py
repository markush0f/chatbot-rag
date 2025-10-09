from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException, status

from .models import User
from .repository import UserRepository
from .schemas import UserCreate


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)
        self.session = session

    def list_with_total(self, offset: int, limit: int) -> tuple[list[User], int]:
        items_seq = self.repo.list(offset=offset, limit=limit)
        items: List[User] = list(items_seq)
        total = self.repo.count()
        return items, total

    def create(self, data: UserCreate) -> User:
        existing_user = self.session.exec(
            select(User).where(User.email == data.email)
        ).first()

        existing_user = self.repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered.",
            )

        obj = User.model_validate(data.model_dump())
        return self.repo.create(obj)
