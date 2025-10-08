from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# ⚙️ Crear el motor de conexión
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Cambia a True si quieres ver los SQL logs
    pool_pre_ping=True,  # Revisa que las conexiones sigan vivas
)


def init_db():
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas o verificadas correctamente.")


def get_session():
    with Session(engine) as session:
        yield session
