"""Smart Parking module models."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class ParkingSlotStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


class ParkingSlot(Base):
    """Represents a single parking slot."""

    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_number = Column(String(20), unique=True, nullable=False, index=True)
    zone = Column(String(50), nullable=False)
    vehicle_type = Column(String(20), nullable=False, default="car")
    status = Column(Enum(ParkingSlotStatus), nullable=False, default=ParkingSlotStatus.AVAILABLE)
    hourly_rate = Column(Float, nullable=False, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("ParkingBooking", back_populates="slot")


class ParkingBooking(Base):
    """Represents a booking of a parking slot by a visitor."""

    __tablename__ = "parking_bookings"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("parking_slots.id"), nullable=False)
    vehicle_number = Column(String(20), nullable=False)
    visitor_name = Column(String(100), nullable=False)
    booked_at = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)

    slot = relationship("ParkingSlot", back_populates="bookings")
