"""Pydantic schemas for the AI Fan Assistant module."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class FAQEntryCreate(BaseModel):
    keywords: str = Field(..., min_length=1, max_length=255)
    question: str = Field(..., min_length=1, max_length=255)
    answer: str = Field(..., min_length=1)
    category: str = Field(default="general", max_length=50)


class FAQEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    keywords: str
    question: str
    answer: str
    category: str
    created_at: datetime


class AssistantQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)


class AssistantQueryResponse(BaseModel):
    query: str
    answer: str
    matched: bool
    category: Optional[str] = None
    confidence: float
