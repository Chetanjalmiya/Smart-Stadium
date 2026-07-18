"""Crowd Density Monitoring module model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database.base import Base


class CrowdDensity(Base):
    """Represents a crowd density reading for a stadium zone."""

    __tablename__ = "crowd_density"

    id = Column(Integer, primary_key=True, index=True)
    zone = Column(String(50), nullable=False, index=True)
    current_count = Column(Integer, nullable=False, default=0)
    capacity = Column(Integer, nullable=False, default=100)
    density_percentage = Column(Float, nullable=False, default=0.0)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
