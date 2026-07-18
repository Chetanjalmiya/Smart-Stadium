"""Business logic for the Seat Finder module."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.seat import Seat
from app.schemas.seat import SeatCreate
from app.utils.exceptions import NotFoundException, ConflictException


class SeatService:
    """Encapsulates seat lookup and availability logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_seat(self, payload: SeatCreate) -> Seat:
        existing = self.db.query(Seat).filter(Seat.seat_number == payload.seat_number).first()
        if existing:
            raise ConflictException(f"Seat '{payload.seat_number}' already exists.")
        seat = Seat(**payload.model_dump())
        self.db.add(seat)
        self.db.commit()
        self.db.refresh(seat)
        return seat

    def find_by_number(self, seat_number: str) -> Seat:
        seat = self.db.query(Seat).filter(Seat.seat_number == seat_number).first()
        if not seat:
            raise NotFoundException("Seat", seat_number)
        return seat

    def list_seats(
        self,
        section: Optional[str] = None,
        available_only: bool = False,
        accessible_only: bool = False,
    ) -> List[Seat]:
        query = self.db.query(Seat)
        if section:
            query = query.filter(Seat.section == section)
        if available_only:
            query = query.filter(Seat.is_occupied.is_(False))
        if accessible_only:
            query = query.filter(Seat.is_accessible.is_(True))
        return query.order_by(Seat.section.asc(), Seat.seat_number.asc()).all()

    def set_occupied(self, seat_number: str, occupied: bool) -> Seat:
        seat = self.find_by_number(seat_number)
        seat.is_occupied = occupied
        self.db.commit()
        self.db.refresh(seat)
        return seat
