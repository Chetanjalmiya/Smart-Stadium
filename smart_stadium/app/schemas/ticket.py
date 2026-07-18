"""Pydantic schemas for the Smart Ticket (QR Code) module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.models.ticket import TicketStatus


class TicketCreate(BaseModel):
    match_id: int = Field(..., gt=0)
    holder_name: str = Field(..., min_length=1, max_length=100)
    holder_email: EmailStr
    seat_number: Optional[str] = Field(default=None, max_length=20)
    section: Optional[str] = Field(default=None, max_length=50)
    gate: Optional[str] = Field(default=None, max_length=20)
    price: float = Field(default=0.0, ge=0)


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_code: str
    match_id: int
    holder_name: str
    holder_email: str
    seat_number: Optional[str] = None
    section: Optional[str] = None
    gate: Optional[str] = None
    price: float
    status: TicketStatus
    qr_code_data: Optional[str] = None
    created_at: datetime
    checked_in_at: Optional[datetime] = None


class TicketVerifyRequest(BaseModel):
    ticket_code: str = Field(..., min_length=1)
