"""Stadium Information module models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.base import Base


class StadiumInfo(Base):
    """Represents general static information about the stadium."""

    __tablename__ = "stadium_info"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Amenity(Base):
    """Represents an amenity/facility available at the stadium."""

    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
