"""Business logic for the Notifications module."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationCategory
from app.schemas.notification import NotificationCreate
from app.utils.exceptions import NotFoundException


class NotificationService:
    """Encapsulates notification broadcast and retrieval logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, payload: NotificationCreate) -> Notification:
        notification = Notification(**payload.model_dump())
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def list_notifications(
        self, category: Optional[NotificationCategory] = None, unread_only: bool = False
    ) -> List[Notification]:
        query = self.db.query(Notification)
        if category:
            query = query.filter(Notification.category == category)
        if unread_only:
            query = query.filter(Notification.is_read.is_(False))
        return query.order_by(Notification.created_at.desc()).all()

    def get_notification(self, notification_id: int) -> Notification:
        notification = (
            self.db.query(Notification).filter(Notification.id == notification_id).first()
        )
        if not notification:
            raise NotFoundException("Notification", notification_id)
        return notification

    def mark_as_read(self, notification_id: int) -> Notification:
        notification = self.get_notification(notification_id)
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification
