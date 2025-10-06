from fastapi import FastAPI
# from app.api.routes.rag_router import router as rag_router

app = FastAPI(title="Chatbot RAG Backend")

# app.include_router(rag_router, prefix="/api/rag", tags=["RAG"])


@app.get("/")
def root():
    return {"message": "Chatbot RAG Backend en marcha"}
