"""Pydantic schemas for Live Match Information & Match Schedule modules."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.match import MatchStatus


class MatchCreate(BaseModel):
    home_team: str = Field(..., min_length=1, max_length=100)
    away_team: str = Field(..., min_length=1, max_length=100)
    venue: str = Field(default="Main Arena", max_length=150)
    scheduled_time: datetime


class MatchUpdate(BaseModel):
    status: Optional[MatchStatus] = None
    home_score: Optional[int] = Field(default=None, ge=0)
    away_score: Optional[int] = Field(default=None, ge=0)
    current_minute: Optional[int] = Field(default=None, ge=0, le=200)
    summary: Optional[str] = None


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    home_team: str
    away_team: str
    venue: str
    scheduled_time: datetime
    status: MatchStatus
    home_score: int
    away_score: int
    current_minute: int
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
