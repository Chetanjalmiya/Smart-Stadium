"""Feedback module model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.base import Base


class Feedback(Base):
    """Represents visitor feedback and ratings."""

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    visitor_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, default="general")
    rating = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
