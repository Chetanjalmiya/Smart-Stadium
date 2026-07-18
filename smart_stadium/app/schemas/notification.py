"""Pydantic schemas for the Notifications module."""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.notification import NotificationCategory


class NotificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    message: str = Field(..., min_length=1)
    category: NotificationCategory = NotificationCategory.GENERAL


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    message: str
    category: NotificationCategory
    is_read: bool
    created_at: datetime
