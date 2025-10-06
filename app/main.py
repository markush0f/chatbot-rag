from fastapi import FastAPI
from app.routers.drive import router as drive_router

app = FastAPI(title="Chatbot RAG Backend")

app.include_router(drive_router)


@app.get("/")
def root():
    return {"message": "Chatbot RAG Backend en marcha"}
