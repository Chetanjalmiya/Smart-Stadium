"""Business logic for Live Match Information & Match Schedule modules."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.match import Match, MatchStatus
from app.schemas.match import MatchCreate, MatchUpdate
from app.utils.exceptions import NotFoundException


class MatchService:
    """Encapsulates match creation, scheduling and live-update logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_match(self, payload: MatchCreate) -> Match:
        match = Match(**payload.model_dump())
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match

    def get_match(self, match_id: int) -> Match:
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise NotFoundException("Match", match_id)
        return match

    def list_matches(self, status: Optional[MatchStatus] = None) -> List[Match]:
        query = self.db.query(Match)
        if status:
            query = query.filter(Match.status == status)
        return query.order_by(Match.scheduled_time.asc()).all()

    def get_live_matches(self) -> List[Match]:
        return (
            self.db.query(Match)
            .filter(Match.status.in_([MatchStatus.LIVE, MatchStatus.HALFTIME]))
            .all()
        )

    def get_schedule(self) -> List[Match]:
        return (
            self.db.query(Match)
            .filter(Match.status == MatchStatus.SCHEDULED)
            .order_by(Match.scheduled_time.asc())
            .all()
        )

    def update_match(self, match_id: int, payload: MatchUpdate) -> Match:
        match = self.get_match(match_id)
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(match, field, value)
        match.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(match)
        return match

    def delete_match(self, match_id: int) -> None:
        match = self.get_match(match_id)
        self.db.delete(match)
        self.db.commit()
