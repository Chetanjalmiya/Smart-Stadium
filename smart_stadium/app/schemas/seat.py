"""Pydantic schemas for the Seat Finder module."""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SeatCreate(BaseModel):
    seat_number: str = Field(..., min_length=1, max_length=20)
    section: str = Field(..., min_length=1, max_length=50)
    row: str = Field(..., min_length=1, max_length=10)
    gate: str = Field(..., min_length=1, max_length=20)
    is_accessible: bool = False
    category: str = Field(default="general", max_length=30)


class SeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seat_number: str
    section: str
    row: str
    gate: str
    is_accessible: bool
    is_occupied: bool
    category: str
    created_at: datetime
