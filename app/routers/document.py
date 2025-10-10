from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.core.database import get_session
from app.domain.document.service import DocumentService
from app.domain.document.schemas import (
    DocumentCreate,
    DocumentRead,
    DocumentPage,
    DocumentUpdate,
)

router = APIRouter(prefix="/document", tags=["document"])


def get_service(session: Session = Depends(get_session)) -> DocumentService:
    return DocumentService(session)


@router.get("", response_model=DocumentPage)
def list_document(
    offset: int = 0,
    limit: int = 50,
    name: str | None = Query(None),
    email: str | None = Query(None),
    status: str | None = Query(None),
    svc: DocumentService = Depends(get_service),
):
    filters = {"name": name, "email": email, "status": status}
    items, total = svc.list_with_total(offset=offset, limit=limit, filters=filters)
    return DocumentPage(total=total, items=items)


@router.get("/<built-in function id>", response_model=DocumentRead)
def get_document(id: int, svc: DocumentService = Depends(get_service)):
    obj = svc.get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Document not found")
    return obj


@router.post("", response_model=DocumentRead)
def create_document(
    payload: DocumentCreate, svc: DocumentService = Depends(get_service)
):
    return svc.create(payload)


@router.put("/<built-in function id>", response_model=DocumentRead)
def update_document(
    id: int, payload: DocumentUpdate, svc: DocumentService = Depends(get_service)
):
    obj = svc.update(id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Document not found")
    return obj


@router.delete("/<built-in function id>")
def delete_document(id: int, svc: DocumentService = Depends(get_service)):
    ok = svc.delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"ok": True}
