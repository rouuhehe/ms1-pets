from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import settings
from typing import Optional

_engine = None
SessionLocal: Optional[sessionmaker] = None


def init_db() -> None:
    """
    Inicializa la base de datos
    """
    global _engine, SessionLocal
    db_url = settings.DATABASE_URL

    if not db_url:
        raise RuntimeError("DATABASE_URL not defined")

    _engine = create_engine(
        db_url,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_pre_ping=True,
        echo=True,
        future=True
    )

    SessionLocal = sessionmaker(
        bind=_engine,
        autocommit=False,
        autoflush=False
    )


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI para inyectar la sesión en cada request
    """
    if SessionLocal is None:
        raise RuntimeError("_SessionLocal not initialized")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
