"""Pydantic schemas for the Emergency SOS module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.sos import SOSType, SOSStatus


class SOSRequestCreate(BaseModel):
    requester_name: str = Field(..., min_length=1, max_length=100)
    contact_number: str = Field(..., min_length=5, max_length=20)
    sos_type: SOSType = SOSType.OTHER
    location: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class SOSRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    requester_name: str
    contact_number: str
    sos_type: SOSType
    location: str
    description: Optional[str] = None
    status: SOSStatus
    created_at: datetime
    resolved_at: Optional[datetime] = None


class SOSStatusUpdate(BaseModel):
    status: SOSStatus
