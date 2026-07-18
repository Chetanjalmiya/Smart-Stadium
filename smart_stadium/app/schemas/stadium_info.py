"""Pydantic schemas for the Stadium Information module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class StadiumInfoCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=150)
    content: str = Field(..., min_length=1)


class StadiumInfoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=150)
    content: Optional[str] = None


class StadiumInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    title: str
    content: str
    updated_at: datetime


class AmenityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class AmenityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    location: str
    description: Optional[str] = None
    created_at: datetime
