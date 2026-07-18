"""Pydantic schemas for the Smart Parking module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.parking import ParkingSlotStatus


class ParkingSlotCreate(BaseModel):
    slot_number: str = Field(..., min_length=1, max_length=20)
    zone: str = Field(..., min_length=1, max_length=50)
    vehicle_type: str = Field(default="car", max_length=20)
    hourly_rate: float = Field(default=5.0, ge=0)


class ParkingSlotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slot_number: str
    zone: str
    vehicle_type: str
    status: ParkingSlotStatus
    hourly_rate: float
    created_at: datetime


class ParkingBookingCreate(BaseModel):
    slot_id: int = Field(..., gt=0)
    vehicle_number: str = Field(..., min_length=1, max_length=20)
    visitor_name: str = Field(..., min_length=1, max_length=100)


class ParkingBookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slot_id: int
    vehicle_number: str
    visitor_name: str
    booked_at: datetime
    released_at: Optional[datetime] = None
    is_active: int
