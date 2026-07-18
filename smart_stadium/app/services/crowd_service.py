"""Business logic for the Crowd Density Monitoring module."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.crowd import CrowdDensity
from app.schemas.crowd import CrowdDensityCreate
from app.utils.exceptions import NotFoundException


def classify_risk(percentage: float) -> str:
    """Classify crowd density risk level based on percentage occupancy."""
    if percentage >= 90:
        return "critical"
    if percentage >= 75:
        return "high"
    if percentage >= 50:
        return "moderate"
    return "normal"


class CrowdService:
    """Encapsulates crowd density recording and risk-level analysis."""

    def __init__(self, db: Session):
        self.db = db

    def record_density(self, payload: CrowdDensityCreate) -> CrowdDensity:
        percentage = round((payload.current_count / payload.capacity) * 100, 2)
        record = CrowdDensity(
            zone=payload.zone,
            current_count=payload.current_count,
            capacity=payload.capacity,
            density_percentage=percentage,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_latest_by_zone(self, zone: str) -> CrowdDensity:
        record = (
            self.db.query(CrowdDensity)
            .filter(CrowdDensity.zone == zone)
            .order_by(CrowdDensity.recorded_at.desc())
            .first()
        )
        if not record:
            raise NotFoundException("Crowd density data for zone", zone)
        return record

    def get_all_latest(self) -> List[CrowdDensity]:
        zones = [row[0] for row in self.db.query(CrowdDensity.zone).distinct().all()]
        results = []
        for zone in zones:
            latest = (
                self.db.query(CrowdDensity)
                .filter(CrowdDensity.zone == zone)
                .order_by(CrowdDensity.recorded_at.desc())
                .first()
            )
            if latest:
                results.append(latest)
        return results

    def get_history(self, zone: Optional[str] = None, limit: int = 50) -> List[CrowdDensity]:
        query = self.db.query(CrowdDensity)
        if zone:
            query = query.filter(CrowdDensity.zone == zone)
        return query.order_by(CrowdDensity.recorded_at.desc()).limit(limit).all()
