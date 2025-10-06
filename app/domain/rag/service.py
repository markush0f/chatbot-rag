import os
import shutil
import io
from pathlib import Path
from app.domain.drive.service import DriveService
from googleapiclient.http import MediaIoBaseDownload

# 📄 Loaders y módulos principales (mantienen langchain_community)
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 🤖 Modelos y embeddings de OpenAI (paquete oficial)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


class RagService:
    def __init__(self):
        self.drive = DriveService()
        self.docs_path = Path("data/docs")
        self.index_path = Path("data/faiss_index")
        self.docs_path.mkdir(parents=True, exist_ok=True)
        self.index_path.mkdir(parents=True, exist_ok=True)

    # Descargar documentos desde Drive (con detección MIME)
    def download_documents(self, file_ids: list[str]):
        for file_id in file_ids:
            try:
                # Obtener nombre y tipo real
                file = (
                    self.drive.service.files()
                    .get(
                        fileId=file_id, fields="name, mimeType", supportsAllDrives=True
                    )
                    .execute()
                )

                name = file["name"]
                mime_type = file["mimeType"]

                # Añadir extensión si falta
                if "." not in name:
                    if mime_type == "application/pdf":
                        name += ".pdf"
                    elif mime_type in (
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "application/msword",
                    ):
                        name += ".docx"
                    elif mime_type.startswith("text/"):
                        name += ".txt"

                local_path = self.docs_path / name

                # Descargar contenido
                request = self.drive.service.files().get_media(
                    fileId=file_id, supportsAllDrives=True
                )
                fh = io.FileIO(local_path, "wb")
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        print(f"⬇️  Descargando {name}: {int(status.progress() * 100)}%")

                print(f"✅ Archivo descargado: {name} ({mime_type})")

            except Exception as e:
                error_msg = str(e)
                if "appNotAuthorizedToFile" in error_msg:
                    print(f"⚠️ Sin permisos para el archivo {file_id}. Omitido.")
                elif "File not found" in error_msg:
                    print(
                        f"⚠️ Archivo no encontrado o ID incorrecto: {file_id}. Omitido."
                    )
                else:
                    print(f"❌ Error inesperado al descargar {file_id}: {e}")

    # Crear embeddings temporales
    def create_embeddings(self):
        all_docs = []
        for file in self.docs_path.iterdir():
            if file.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file))
            elif file.suffix.lower() == ".docx":
                loader = Docx2txtLoader(str(file))
            elif file.suffix.lower() in [".txt", ".md"]:
                loader = TextLoader(str(file))
            else:
                print(f"⚠️ Tipo no soportado: {file.name}")
                continue

            docs = loader.load()
            all_docs.extend(docs)

        if not all_docs:
            raise ValueError("❌ No se encontraron documentos válidos para procesar.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(all_docs)

        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(chunks, embeddings)
        db.save_local(str(self.index_path))
        print("✅ Embeddings creados y almacenados temporalmente.")
        return db

    # Consultar el RAG
    def query(self, question: str):
        embeddings = OpenAIEmbeddings()
        db = FAISS.load_local(
            str(self.index_path), embeddings, allow_dangerous_deserialization=True
        )

        retriever = db.as_retriever(search_kwargs={"k": 4})

        # 🔥 Modelo actualizado (usa gpt-4o-mini por defecto)
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

        qa = RetrievalQA.from_chain_type(
            llm=llm, retriever=retriever, chain_type="stuff"
        )

        result = qa.invoke(
            {
                "query": question,
            }
        )["result"]
        return result

    # Limpiar documentos e índice temporal
    def cleanup(self):
        shutil.rmtree(self.docs_path, ignore_errors=True)
        shutil.rmtree(self.index_path, ignore_errors=True)
        self.docs_path.mkdir(parents=True, exist_ok=True)
        self.index_path.mkdir(parents=True, exist_ok=True)
        print("🧹 Limpieza completada (docs + embeddings).")

    # 5️⃣ Flujo completo
    def run_pipeline(self, question: str, file_ids: list[str]):
        self.download_documents(file_ids)
        self.create_embeddings()
        answer = self.query(question)
        self.cleanup()
        return answer
