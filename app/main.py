from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db
from app.routers.drive import router as drive_router
from app.routers.rag import router as rag_router
from app.routers.user import router as user_router
from app.routers.chat import router as chat_router
from app.routers.message import router as message_router

app = FastAPI(title="Chatbot RAG Backend")

app.include_router(drive_router)
app.include_router(rag_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicación Crecenia Chatbot...")
    init_db()  
    yield
    print("Cerrando aplicación Crecenia Chatbot...")


@app.get("/")
def root():
    return {"message": "Chatbot RAG Backend en marcha"}
