"""Weather Alerts module model."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from app.database.base import Base


class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"


class WeatherAlert(Base):
    """Represents a weather advisory issued for the stadium."""

    __tablename__ = "weather_alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False, default=AlertSeverity.LOW)
    temperature_celsius = Column(String(10), nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
