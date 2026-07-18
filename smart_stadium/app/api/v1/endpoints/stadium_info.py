"""API routes for the Stadium Information module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.stadium_info_service import StadiumInfoService
from app.schemas.stadium_info import (
    StadiumInfoCreate,
    StadiumInfoUpdate,
    StadiumInfoResponse,
    AmenityCreate,
    AmenityResponse,
)
from app.utils.responses import success_response

router = APIRouter(prefix="/stadium-info", tags=["Stadium Information"])


@router.post("", response_model=dict, status_code=201, summary="Create stadium info entry")
def create_info(payload: StadiumInfoCreate, db: Session = Depends(get_db)) -> dict:
    info = StadiumInfoService(db).create_info(payload)
    return success_response(StadiumInfoResponse.model_validate(info).model_dump(), "Stadium info created.")


@router.get("", response_model=dict, summary="List all stadium info entries")
def list_info(db: Session = Depends(get_db)) -> dict:
    entries = StadiumInfoService(db).list_info()
    data = [StadiumInfoResponse.model_validate(e).model_dump() for e in entries]
    return success_response(data, f"Retrieved {len(data)} info entr(y/ies).")


@router.get("/amenities", response_model=dict, summary="List stadium amenities")
def list_amenities(category: Optional[str] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    amenities = StadiumInfoService(db).list_amenities(category)
    data = [AmenityResponse.model_validate(a).model_dump() for a in amenities]
    return success_response(data, f"Retrieved {len(data)} amenit(y/ies).")


@router.post("/amenities", response_model=dict, status_code=201, summary="Add a stadium amenity")
def create_amenity(payload: AmenityCreate, db: Session = Depends(get_db)) -> dict:
    amenity = StadiumInfoService(db).create_amenity(payload)
    return success_response(AmenityResponse.model_validate(amenity).model_dump(), "Amenity added successfully.")


@router.get("/{key}", response_model=dict, summary="Get stadium info by key")
def get_info(key: str, db: Session = Depends(get_db)) -> dict:
    info = StadiumInfoService(db).get_info(key)
    return success_response(StadiumInfoResponse.model_validate(info).model_dump())


@router.put("/{key}", response_model=dict, summary="Update stadium info by key")
def update_info(key: str, payload: StadiumInfoUpdate, db: Session = Depends(get_db)) -> dict:
    info = StadiumInfoService(db).update_info(key, payload)
    return success_response(StadiumInfoResponse.model_validate(info).model_dump(), "Stadium info updated.")
