"""Business logic for the Feedback module."""
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


class FeedbackService:
    """Encapsulates feedback submission and aggregation logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, payload: FeedbackCreate) -> Feedback:
        feedback = Feedback(**payload.model_dump())
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def list_feedback(self, category: Optional[str] = None) -> List[Feedback]:
        query = self.db.query(Feedback)
        if category:
            query = query.filter(Feedback.category == category)
        return query.order_by(Feedback.created_at.desc()).all()

    def get_average_rating(self, category: Optional[str] = None) -> dict:
        query = self.db.query(func.avg(Feedback.rating), func.count(Feedback.id))
        if category:
            query = query.filter(Feedback.category == category)
        avg_rating, total = query.first()
        return {
            "category": category or "all",
            "average_rating": round(avg_rating, 2) if avg_rating else 0.0,
            "total_responses": total or 0,
        }
