"""Pydantic schemas for the Feedback module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class FeedbackCreate(BaseModel):
    visitor_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(default="general", max_length=50)
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    visitor_name: str
    category: str
    rating: int
    comments: Optional[str] = None
    created_at: datetime
