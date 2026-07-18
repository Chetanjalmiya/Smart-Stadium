"""API routes for the Feedback module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.feedback_service import FeedbackService
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.utils.responses import success_response

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("", response_model=dict, status_code=201, summary="Submit feedback")
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)) -> dict:
    feedback = FeedbackService(db).create_feedback(payload)
    return success_response(FeedbackResponse.model_validate(feedback).model_dump(), "Feedback submitted. Thank you!")


@router.get("", response_model=dict, summary="List feedback entries")
def list_feedback(category: Optional[str] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    entries = FeedbackService(db).list_feedback(category)
    data = [FeedbackResponse.model_validate(f).model_dump() for f in entries]
    return success_response(data, f"Retrieved {len(data)} feedback entr(y/ies).")


@router.get("/summary", response_model=dict, summary="Get average rating summary")
def get_summary(category: Optional[str] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    summary = FeedbackService(db).get_average_rating(category)
    return success_response(summary)
