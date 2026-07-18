"""Pydantic schemas for the Weather Alerts module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.weather import AlertSeverity


class WeatherAlertCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1)
    severity: AlertSeverity = AlertSeverity.LOW
    temperature_celsius: Optional[str] = Field(default=None, max_length=10)
    expires_at: Optional[datetime] = None


class WeatherAlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    severity: AlertSeverity
    temperature_celsius: Optional[str] = None
    is_active: int
    issued_at: datetime
    expires_at: Optional[datetime] = None
