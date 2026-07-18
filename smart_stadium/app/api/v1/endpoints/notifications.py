"""API routes for the Notifications module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.models.notification import NotificationCategory
from app.utils.responses import success_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("", response_model=dict, status_code=201, summary="Broadcast a notification")
def create_notification(payload: NotificationCreate, db: Session = Depends(get_db)) -> dict:
    notification = NotificationService(db).create_notification(payload)
    return success_response(
        NotificationResponse.model_validate(notification).model_dump(), "Notification broadcast successfully."
    )


@router.get("", response_model=dict, summary="List notifications")
def list_notifications(
    category: Optional[NotificationCategory] = Query(default=None),
    unread_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    notifications = NotificationService(db).list_notifications(category, unread_only)
    data = [NotificationResponse.model_validate(n).model_dump() for n in notifications]
    return success_response(data, f"Retrieved {len(data)} notification(s).")


@router.post("/{notification_id}/read", response_model=dict, summary="Mark notification as read")
def mark_read(notification_id: int, db: Session = Depends(get_db)) -> dict:
    notification = NotificationService(db).mark_as_read(notification_id)
    return success_response(
        NotificationResponse.model_validate(notification).model_dump(), "Notification marked as read."
    )
