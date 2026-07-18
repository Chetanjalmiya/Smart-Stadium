"""Business logic for the Emergency SOS module."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sos import SOSRequest, SOSStatus
from app.schemas.sos import SOSRequestCreate, SOSStatusUpdate
from app.utils.exceptions import NotFoundException


class SOSService:
    """Encapsulates emergency SOS request lifecycle management."""

    def __init__(self, db: Session):
        self.db = db

    def create_sos(self, payload: SOSRequestCreate) -> SOSRequest:
        sos = SOSRequest(**payload.model_dump())
        self.db.add(sos)
        self.db.commit()
        self.db.refresh(sos)
        return sos

    def get_sos(self, sos_id: int) -> SOSRequest:
        sos = self.db.query(SOSRequest).filter(SOSRequest.id == sos_id).first()
        if not sos:
            raise NotFoundException("SOS request", sos_id)
        return sos

    def list_sos(self, status: Optional[SOSStatus] = None) -> List[SOSRequest]:
        query = self.db.query(SOSRequest)
        if status:
            query = query.filter(SOSRequest.status == status)
        return query.order_by(SOSRequest.created_at.desc()).all()

    def update_status(self, sos_id: int, payload: SOSStatusUpdate) -> SOSRequest:
        sos = self.get_sos(sos_id)
        sos.status = payload.status
        if payload.status == SOSStatus.RESOLVED:
            sos.resolved_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(sos)
        return sos
