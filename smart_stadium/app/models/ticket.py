"""Smart Ticket module model."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.base import Base


class TicketStatus(str, enum.Enum):
    VALID = "valid"
    USED = "used"
    CANCELLED = "cancelled"


class Ticket(Base):
    """Represents a stadium entry ticket bound to a QR code."""

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_code = Column(String(50), unique=True, nullable=False, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    holder_name = Column(String(100), nullable=False)
    holder_email = Column(String(150), nullable=False)
    seat_number = Column(String(20), nullable=True)
    section = Column(String(50), nullable=True)
    gate = Column(String(20), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.VALID)
    qr_code_data = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    checked_in_at = Column(DateTime, nullable=True)

    match = relationship("Match")
