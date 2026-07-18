"""Lost & Found module model."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from app.database.base import Base


class LostFoundStatus(str, enum.Enum):
    REPORTED = "reported"
    FOUND = "found"
    CLAIMED = "claimed"


class LostFoundType(str, enum.Enum):
    LOST = "lost"
    FOUND = "found"


class LostFoundItem(Base):
    """Represents a lost or found item report."""

    __tablename__ = "lost_found_items"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(Enum(LostFoundType), nullable=False)
    item_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=False)
    reporter_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    status = Column(Enum(LostFoundStatus), nullable=False, default=LostFoundStatus.REPORTED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
