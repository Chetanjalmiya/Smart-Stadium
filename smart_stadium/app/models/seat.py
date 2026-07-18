"""Seat Finder module model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database.base import Base


class Seat(Base):
    """Represents a physical seat in the stadium."""

    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String(20), unique=True, nullable=False, index=True)
    section = Column(String(50), nullable=False)
    row = Column(String(10), nullable=False)
    gate = Column(String(20), nullable=False)
    is_accessible = Column(Boolean, default=False)
    is_occupied = Column(Boolean, default=False)
    category = Column(String(30), nullable=False, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
