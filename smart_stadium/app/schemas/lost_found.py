"""Pydantic schemas for the Lost & Found module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.lost_found import LostFoundStatus, LostFoundType


class LostFoundItemCreate(BaseModel):
    item_type: LostFoundType
    item_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    location: str = Field(..., min_length=1, max_length=100)
    reporter_name: str = Field(..., min_length=1, max_length=100)
    contact_number: str = Field(..., min_length=5, max_length=20)


class LostFoundItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_type: LostFoundType
    item_name: str
    description: Optional[str] = None
    location: str
    reporter_name: str
    contact_number: str
    status: LostFoundStatus
    created_at: datetime
    updated_at: datetime


class LostFoundStatusUpdate(BaseModel):
    status: LostFoundStatus
