"""Business logic for the Smart Parking module."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.parking import ParkingSlot, ParkingBooking, ParkingSlotStatus
from app.schemas.parking import ParkingSlotCreate, ParkingBookingCreate
from app.utils.exceptions import NotFoundException, ConflictException


class ParkingService:
    """Encapsulates parking slot management and booking logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_slot(self, payload: ParkingSlotCreate) -> ParkingSlot:
        existing = (
            self.db.query(ParkingSlot)
            .filter(ParkingSlot.slot_number == payload.slot_number)
            .first()
        )
        if existing:
            raise ConflictException(f"Parking slot '{payload.slot_number}' already exists.")
        slot = ParkingSlot(**payload.model_dump())
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def list_slots(
        self, zone: Optional[str] = None, status: Optional[ParkingSlotStatus] = None
    ) -> List[ParkingSlot]:
        query = self.db.query(ParkingSlot)
        if zone:
            query = query.filter(ParkingSlot.zone == zone)
        if status:
            query = query.filter(ParkingSlot.status == status)
        return query.order_by(ParkingSlot.slot_number.asc()).all()

    def get_slot(self, slot_id: int) -> ParkingSlot:
        slot = self.db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
        if not slot:
            raise NotFoundException("Parking slot", slot_id)
        return slot

    def book_slot(self, payload: ParkingBookingCreate) -> ParkingBooking:
        slot = self.get_slot(payload.slot_id)
        if slot.status != ParkingSlotStatus.AVAILABLE:
            raise ConflictException(f"Parking slot '{slot.slot_number}' is not available.")

        booking = ParkingBooking(
            slot_id=payload.slot_id,
            vehicle_number=payload.vehicle_number,
            visitor_name=payload.visitor_name,
        )
        slot.status = ParkingSlotStatus.OCCUPIED
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def release_booking(self, booking_id: int) -> ParkingBooking:
        booking = self.db.query(ParkingBooking).filter(ParkingBooking.id == booking_id).first()
        if not booking:
            raise NotFoundException("Parking booking", booking_id)
        if not booking.is_active:
            raise ConflictException("This parking booking has already been released.")

        booking.is_active = 0
        booking.released_at = datetime.utcnow()
        slot = self.get_slot(booking.slot_id)
        slot.status = ParkingSlotStatus.AVAILABLE
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_availability_summary(self) -> dict:
        total = self.db.query(ParkingSlot).count()
        available = (
            self.db.query(ParkingSlot)
            .filter(ParkingSlot.status == ParkingSlotStatus.AVAILABLE)
            .count()
        )
        occupied = (
            self.db.query(ParkingSlot)
            .filter(ParkingSlot.status == ParkingSlotStatus.OCCUPIED)
            .count()
        )
        return {"total_slots": total, "available": available, "occupied": occupied}
