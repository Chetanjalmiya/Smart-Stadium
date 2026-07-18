"""Stadium Navigation module models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from app.database.base import Base


class NavigationPoint(Base):
    """Represents a navigable point of interest inside the stadium."""

    __tablename__ = "navigation_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    zone = Column(String(50), nullable=False)
    floor = Column(String(20), nullable=False, default="Ground")
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
