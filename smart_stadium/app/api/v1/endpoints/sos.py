"""API routes for the Emergency SOS module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.sos_service import SOSService
from app.schemas.sos import SOSRequestCreate, SOSRequestResponse, SOSStatusUpdate
from app.models.sos import SOSStatus
from app.utils.responses import success_response

router = APIRouter(prefix="/sos", tags=["Emergency SOS"])


@router.post("", response_model=dict, status_code=201, summary="Raise an emergency SOS request")
def create_sos(payload: SOSRequestCreate, db: Session = Depends(get_db)) -> dict:
    sos = SOSService(db).create_sos(payload)
    return success_response(
        SOSRequestResponse.model_validate(sos).model_dump(),
        "Emergency SOS request received. Help is on the way.",
    )


@router.get("", response_model=dict, summary="List SOS requests")
def list_sos(status: Optional[SOSStatus] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    requests = SOSService(db).list_sos(status)
    data = [SOSRequestResponse.model_validate(r).model_dump() for r in requests]
    return success_response(data, f"Retrieved {len(data)} SOS request(s).")


@router.get("/{sos_id}", response_model=dict, summary="Get SOS request by ID")
def get_sos(sos_id: int, db: Session = Depends(get_db)) -> dict:
    sos = SOSService(db).get_sos(sos_id)
    return success_response(SOSRequestResponse.model_validate(sos).model_dump())


@router.patch("/{sos_id}/status", response_model=dict, summary="Update SOS request status")
def update_sos_status(sos_id: int, payload: SOSStatusUpdate, db: Session = Depends(get_db)) -> dict:
    sos = SOSService(db).update_status(sos_id, payload)
    return success_response(SOSRequestResponse.model_validate(sos).model_dump(), "SOS status updated.")
