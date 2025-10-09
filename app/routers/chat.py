from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.domain.chat.service import ChatService
from app.domain.chat.schemas import ChatCreate, ChatRead, ChatPage

router = APIRouter(prefix="/chat", tags=["chat"])

def get_service(session: Session = Depends(get_session)) -> ChatService:
    return ChatService(session)

@router.get("", response_model=ChatPage)
def list_chat(offset: int = 0, limit: int = 50, svc: ChatService = Depends(get_service)):
    items, total = svc.list_with_total(offset=offset, limit=limit)
    return ChatPage(total=total, items=items)

@router.post("", response_model=ChatRead)
def create_chat(payload: ChatCreate, svc: ChatService = Depends(get_service)):
    return svc.create(payload)

@router.get("/user/{user_id}", response_model=List[ChatRead])
def list_user_chats(user_id: int, session: Session = Depends(get_session)):
    service = ChatService(session)
    return service.list_by_user(user_id)