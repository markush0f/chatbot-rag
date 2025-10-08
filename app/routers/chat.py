from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
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
