"""Notifications module model."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Boolean
from app.database.base import Base


class NotificationCategory(str, enum.Enum):
    GENERAL = "general"
    MATCH = "match"
    SAFETY = "safety"
    PARKING = "parking"
    FOOD = "food"
    WEATHER = "weather"


class Notification(Base):
    """Represents a broadcast notification sent to stadium visitors."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(Enum(NotificationCategory), nullable=False, default=NotificationCategory.GENERAL)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
