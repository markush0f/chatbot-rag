from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.domain.message.service import MessageService
from app.domain.message.schemas import MessageCreate, MessageRead, MessagePage

router = APIRouter(prefix="/message", tags=["message"])

def get_service(session: Session = Depends(get_session)) -> MessageService:
    return MessageService(session)

@router.get("", response_model=MessagePage)
def list_message(offset: int = 0, limit: int = 50, svc: MessageService = Depends(get_service)):
    items, total = svc.list_with_total(offset=offset, limit=limit)
    return MessagePage(total=total, items=items)

@router.post("", response_model=MessageRead)
def create_message(payload: MessageCreate, svc: MessageService = Depends(get_service)):
    return svc.create(payload)
