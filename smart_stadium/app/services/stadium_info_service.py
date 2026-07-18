"""Business logic for the Stadium Information module."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.stadium_info import StadiumInfo, Amenity
from app.schemas.stadium_info import StadiumInfoCreate, StadiumInfoUpdate, AmenityCreate
from app.utils.exceptions import NotFoundException, ConflictException


class StadiumInfoService:
    """Encapsulates general stadium information and amenity management."""

    def __init__(self, db: Session):
        self.db = db

    def create_info(self, payload: StadiumInfoCreate) -> StadiumInfo:
        existing = self.db.query(StadiumInfo).filter(StadiumInfo.key == payload.key).first()
        if existing:
            raise ConflictException(f"Stadium info with key '{payload.key}' already exists.")
        info = StadiumInfo(**payload.model_dump())
        self.db.add(info)
        self.db.commit()
        self.db.refresh(info)
        return info

    def list_info(self) -> List[StadiumInfo]:
        return self.db.query(StadiumInfo).order_by(StadiumInfo.key.asc()).all()

    def get_info(self, key: str) -> StadiumInfo:
        info = self.db.query(StadiumInfo).filter(StadiumInfo.key == key).first()
        if not info:
            raise NotFoundException("Stadium info", key)
        return info

    def update_info(self, key: str, payload: StadiumInfoUpdate) -> StadiumInfo:
        info = self.get_info(key)
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(info, field, value)
        self.db.commit()
        self.db.refresh(info)
        return info

    def create_amenity(self, payload: AmenityCreate) -> Amenity:
        amenity = Amenity(**payload.model_dump())
        self.db.add(amenity)
        self.db.commit()
        self.db.refresh(amenity)
        return amenity

    def list_amenities(self, category: Optional[str] = None) -> List[Amenity]:
        query = self.db.query(Amenity)
        if category:
            query = query.filter(Amenity.category == category)
        return query.order_by(Amenity.name.asc()).all()
