
import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Cargar variables de entorno desde .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edugestion.db")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
