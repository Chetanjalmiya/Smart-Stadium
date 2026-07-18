"""Pydantic schemas for the Crowd Density Monitoring module."""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CrowdDensityCreate(BaseModel):
    zone: str = Field(..., min_length=1, max_length=50)
    current_count: int = Field(..., ge=0)
    capacity: int = Field(..., gt=0)


class CrowdDensityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone: str
    current_count: int
    capacity: int
    density_percentage: float
    recorded_at: datetime
    risk_level: str = "normal"
