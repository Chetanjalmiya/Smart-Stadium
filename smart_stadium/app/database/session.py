"""Database session dependency for FastAPI routes."""
from typing import Generator
from sqlalchemy.orm import Session
from app.database.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
