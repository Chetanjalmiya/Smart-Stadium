"""Business logic for the Lost & Found module."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.lost_found import LostFoundItem, LostFoundStatus, LostFoundType
from app.schemas.lost_found import LostFoundItemCreate, LostFoundStatusUpdate
from app.utils.exceptions import NotFoundException


class LostFoundService:
    """Encapsulates lost & found item reporting and matching logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_item(self, payload: LostFoundItemCreate) -> LostFoundItem:
        item = LostFoundItem(**payload.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_item(self, item_id: int) -> LostFoundItem:
        item = self.db.query(LostFoundItem).filter(LostFoundItem.id == item_id).first()
        if not item:
            raise NotFoundException("Lost & found item", item_id)
        return item

    def list_items(
        self,
        item_type: Optional[LostFoundType] = None,
        status: Optional[LostFoundStatus] = None,
    ) -> List[LostFoundItem]:
        query = self.db.query(LostFoundItem)
        if item_type:
            query = query.filter(LostFoundItem.item_type == item_type)
        if status:
            query = query.filter(LostFoundItem.status == status)
        return query.order_by(LostFoundItem.created_at.desc()).all()

    def search_items(self, keyword: str) -> List[LostFoundItem]:
        pattern = f"%{keyword}%"
        return (
            self.db.query(LostFoundItem)
            .filter(LostFoundItem.item_name.ilike(pattern))
            .order_by(LostFoundItem.created_at.desc())
            .all()
        )

    def update_status(self, item_id: int, payload: LostFoundStatusUpdate) -> LostFoundItem:
        item = self.get_item(item_id)
        item.status = payload.status
        self.db.commit()
        self.db.refresh(item)
        return item
