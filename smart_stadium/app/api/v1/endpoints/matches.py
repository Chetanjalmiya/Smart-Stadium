"""API routes for Live Match Information & Match Schedule modules."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.match_service import MatchService
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse
from app.models.match import MatchStatus
from app.utils.responses import success_response

router = APIRouter(prefix="/matches", tags=["Live Match Information & Schedule"])


@router.post("", response_model=dict, status_code=201, summary="Create a new match")
def create_match(payload: MatchCreate, db: Session = Depends(get_db)) -> dict:
    match = MatchService(db).create_match(payload)
    return success_response(MatchResponse.model_validate(match).model_dump(), "Match created successfully.")


@router.get("", response_model=dict, summary="List all matches")
def list_matches(status: Optional[MatchStatus] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    matches = MatchService(db).list_matches(status)
    data = [MatchResponse.model_validate(m).model_dump() for m in matches]
    return success_response(data, f"Retrieved {len(data)} match(es).")


@router.get("/live", response_model=dict, summary="Get currently live matches")
def get_live_matches(db: Session = Depends(get_db)) -> dict:
    matches = MatchService(db).get_live_matches()
    data = [MatchResponse.model_validate(m).model_dump() for m in matches]
    return success_response(data, f"Retrieved {len(data)} live match(es).")


@router.get("/schedule", response_model=dict, summary="Get upcoming match schedule")
def get_schedule(db: Session = Depends(get_db)) -> dict:
    matches = MatchService(db).get_schedule()
    data = [MatchResponse.model_validate(m).model_dump() for m in matches]
    return success_response(data, f"Retrieved {len(data)} scheduled match(es).")


@router.get("/{match_id}", response_model=dict, summary="Get match by ID")
def get_match(match_id: int, db: Session = Depends(get_db)) -> dict:
    match = MatchService(db).get_match(match_id)
    return success_response(MatchResponse.model_validate(match).model_dump())


@router.patch("/{match_id}", response_model=dict, summary="Update match details or live score")
def update_match(match_id: int, payload: MatchUpdate, db: Session = Depends(get_db)) -> dict:
    match = MatchService(db).update_match(match_id, payload)
    return success_response(MatchResponse.model_validate(match).model_dump(), "Match updated successfully.")


@router.delete("/{match_id}", response_model=dict, summary="Delete a match")
def delete_match(match_id: int, db: Session = Depends(get_db)) -> dict:
    MatchService(db).delete_match(match_id)
    return success_response(None, "Match deleted successfully.")
