
from fastapi import APIRouter, Form
from app.domain.drive.service import DriveService

router = APIRouter(prefix="/drive", tags=["drive"])

svc = DriveService()

@router.post("/process")
def process_data(data: str = Form(...)):
    result = svc.process(data)
    return {"result": result}
