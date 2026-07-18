"""API routes for the Smart Parking module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.parking_service import ParkingService
from app.schemas.parking import (
    ParkingSlotCreate,
    ParkingSlotResponse,
    ParkingBookingCreate,
    ParkingBookingResponse,
)
from app.models.parking import ParkingSlotStatus
from app.utils.responses import success_response

router = APIRouter(prefix="/parking", tags=["Smart Parking"])


@router.post("/slots", response_model=dict, status_code=201, summary="Create a parking slot")
def create_slot(payload: ParkingSlotCreate, db: Session = Depends(get_db)) -> dict:
    slot = ParkingService(db).create_slot(payload)
    return success_response(ParkingSlotResponse.model_validate(slot).model_dump(), "Parking slot created.")


@router.get("/slots", response_model=dict, summary="List parking slots")
def list_slots(
    zone: Optional[str] = Query(default=None),
    status: Optional[ParkingSlotStatus] = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    slots = ParkingService(db).list_slots(zone, status)
    data = [ParkingSlotResponse.model_validate(s).model_dump() for s in slots]
    return success_response(data, f"Retrieved {len(data)} parking slot(s).")


@router.get("/availability", response_model=dict, summary="Get parking availability summary")
def get_availability(db: Session = Depends(get_db)) -> dict:
    summary = ParkingService(db).get_availability_summary()
    return success_response(summary)


@router.post("/bookings", response_model=dict, status_code=201, summary="Book a parking slot")
def book_slot(payload: ParkingBookingCreate, db: Session = Depends(get_db)) -> dict:
    booking = ParkingService(db).book_slot(payload)
    return success_response(
        ParkingBookingResponse.model_validate(booking).model_dump(), "Parking slot booked successfully."
    )


@router.post("/bookings/{booking_id}/release", response_model=dict, summary="Release a parking booking")
def release_booking(booking_id: int, db: Session = Depends(get_db)) -> dict:
    booking = ParkingService(db).release_booking(booking_id)
    return success_response(
        ParkingBookingResponse.model_validate(booking).model_dump(), "Parking slot released successfully."
    )
