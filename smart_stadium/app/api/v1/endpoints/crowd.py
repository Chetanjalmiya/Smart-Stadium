"""API routes for the Crowd Density Monitoring module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.crowd_service import CrowdService, classify_risk
from app.schemas.crowd import CrowdDensityCreate, CrowdDensityResponse
from app.utils.responses import success_response

router = APIRouter(prefix="/crowd", tags=["Crowd Density Monitoring"])


def _to_response(record) -> dict:
    data = CrowdDensityResponse.model_validate(record).model_dump()
    data["risk_level"] = classify_risk(record.density_percentage)
    return data


@router.post("", response_model=dict, status_code=201, summary="Record a crowd density reading")
def record_density(payload: CrowdDensityCreate, db: Session = Depends(get_db)) -> dict:
    record = CrowdService(db).record_density(payload)
    return success_response(_to_response(record), "Crowd density recorded successfully.")


@router.get("/latest", response_model=dict, summary="Get latest density for all zones")
def get_all_latest(db: Session = Depends(get_db)) -> dict:
    records = CrowdService(db).get_all_latest()
    data = [_to_response(r) for r in records]
    return success_response(data, f"Retrieved latest density for {len(data)} zone(s).")


@router.get("/{zone}", response_model=dict, summary="Get latest density for a zone")
def get_latest_by_zone(zone: str, db: Session = Depends(get_db)) -> dict:
    record = CrowdService(db).get_latest_by_zone(zone)
    return success_response(_to_response(record))


@router.get("/{zone}/history", response_model=dict, summary="Get density history for a zone")
def get_history(zone: str, limit: int = Query(default=50, ge=1, le=500), db: Session = Depends(get_db)) -> dict:
    records = CrowdService(db).get_history(zone, limit)
    data = [_to_response(r) for r in records]
    return success_response(data, f"Retrieved {len(data)} history record(s).")
