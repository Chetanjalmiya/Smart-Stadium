"""Emergency SOS module model."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from app.database.base import Base


class SOSType(str, enum.Enum):
    MEDICAL = "medical"
    SECURITY = "security"
    FIRE = "fire"
    LOST_CHILD = "lost_child"
    OTHER = "other"


class SOSStatus(str, enum.Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class SOSRequest(Base):
    """Represents an emergency SOS request raised by a visitor."""

    __tablename__ = "sos_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    sos_type = Column(Enum(SOSType), nullable=False, default=SOSType.OTHER)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(SOSStatus), nullable=False, default=SOSStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
