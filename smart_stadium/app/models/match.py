"""Match and schedule models — Live Match Information & Match Schedule modules."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from app.database.base import Base


class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    HALFTIME = "halftime"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


class Match(Base):
    """Represents a stadium match/event with live and schedule data."""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    venue = Column(String(150), nullable=False, default="Main Arena")
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(Enum(MatchStatus), nullable=False, default=MatchStatus.SCHEDULED)
    home_score = Column(Integer, nullable=False, default=0)
    away_score = Column(Integer, nullable=False, default=0)
    current_minute = Column(Integer, nullable=False, default=0)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
