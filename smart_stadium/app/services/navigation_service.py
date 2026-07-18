"""Business logic for the Stadium Navigation module."""
import math
from typing import List
from sqlalchemy.orm import Session
from app.models.navigation import NavigationPoint
from app.schemas.navigation import NavigationPointCreate, RouteResponse
from app.utils.exceptions import NotFoundException

WALKING_SPEED_UNITS_PER_MINUTE = 60.0


class NavigationService:
    """Encapsulates stadium navigation points and routing logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_point(self, payload: NavigationPointCreate) -> NavigationPoint:
        point = NavigationPoint(**payload.model_dump())
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)
        return point

    def get_point(self, point_id: int) -> NavigationPoint:
        point = self.db.query(NavigationPoint).filter(NavigationPoint.id == point_id).first()
        if not point:
            raise NotFoundException("Navigation point", point_id)
        return point

    def list_points(self, category: str | None = None, zone: str | None = None) -> List[NavigationPoint]:
        query = self.db.query(NavigationPoint)
        if category:
            query = query.filter(NavigationPoint.category == category)
        if zone:
            query = query.filter(NavigationPoint.zone == zone)
        return query.order_by(NavigationPoint.name.asc()).all()

    def get_route(self, origin_id: int, destination_id: int) -> RouteResponse:
        origin = self.get_point(origin_id)
        destination = self.get_point(destination_id)

        distance = math.sqrt(
            (destination.pos_x - origin.pos_x) ** 2 + (destination.pos_y - origin.pos_y) ** 2
        )
        estimated_minutes = round(distance / WALKING_SPEED_UNITS_PER_MINUTE, 1)

        return RouteResponse(
            origin=origin,
            destination=destination,
            distance_units=round(distance, 2),
            estimated_walk_minutes=max(estimated_minutes, 0.5),
            path=[origin, destination],
        )
