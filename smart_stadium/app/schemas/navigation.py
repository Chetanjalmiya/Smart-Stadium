"""Pydantic schemas for the Stadium Navigation module."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class NavigationPointCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    zone: str = Field(..., min_length=1, max_length=50)
    floor: str = Field(default="Ground", max_length=20)
    pos_x: float
    pos_y: float
    description: Optional[str] = None


class NavigationPointResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    zone: str
    floor: str
    pos_x: float
    pos_y: float
    description: Optional[str] = None
    created_at: datetime


class RouteResponse(BaseModel):
    origin: NavigationPointResponse
    destination: NavigationPointResponse
    distance_units: float
    estimated_walk_minutes: float
    path: List[NavigationPointResponse]
