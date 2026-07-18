"""API routes for the Seat Finder module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.seat_service import SeatService
from app.schemas.seat import SeatCreate, SeatResponse
from app.utils.responses import success_response

router = APIRouter(prefix="/seats", tags=["Seat Finder"])


@router.post("", response_model=dict, status_code=201, summary="Register a new seat")
def create_seat(payload: SeatCreate, db: Session = Depends(get_db)) -> dict:
    seat = SeatService(db).create_seat(payload)
    return success_response(SeatResponse.model_validate(seat).model_dump(), "Seat registered successfully.")


@router.get("", response_model=dict, summary="List/find seats with filters")
def list_seats(
    section: Optional[str] = Query(default=None),
    available_only: bool = Query(default=False),
    accessible_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    seats = SeatService(db).list_seats(section, available_only, accessible_only)
    data = [SeatResponse.model_validate(s).model_dump() for s in seats]
    return success_response(data, f"Found {len(data)} seat(s).")


@router.get("/{seat_number}", response_model=dict, summary="Find a seat by seat number")
def find_seat(seat_number: str, db: Session = Depends(get_db)) -> dict:
    seat = SeatService(db).find_by_number(seat_number)
    return success_response(SeatResponse.model_validate(seat).model_dump())


@router.patch("/{seat_number}/occupancy", response_model=dict, summary="Update seat occupancy")
def set_occupancy(seat_number: str, occupied: bool, db: Session = Depends(get_db)) -> dict:
    seat = SeatService(db).set_occupied(seat_number, occupied)
    return success_response(SeatResponse.model_validate(seat).model_dump(), "Seat occupancy updated.")
