"""API routes for the Stadium Navigation module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.navigation_service import NavigationService
from app.schemas.navigation import NavigationPointCreate, NavigationPointResponse, RouteResponse
from app.utils.responses import success_response

router = APIRouter(prefix="/navigation", tags=["Stadium Navigation"])


@router.post("/points", response_model=dict, status_code=201, summary="Create a navigation point")
def create_point(payload: NavigationPointCreate, db: Session = Depends(get_db)) -> dict:
    point = NavigationService(db).create_point(payload)
    return success_response(
        NavigationPointResponse.model_validate(point).model_dump(), "Navigation point created."
    )


@router.get("/points", response_model=dict, summary="List navigation points")
def list_points(
    category: Optional[str] = Query(default=None),
    zone: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    points = NavigationService(db).list_points(category, zone)
    data = [NavigationPointResponse.model_validate(p).model_dump() for p in points]
    return success_response(data, f"Retrieved {len(data)} navigation point(s).")


@router.get("/points/{point_id}", response_model=dict, summary="Get a navigation point")
def get_point(point_id: int, db: Session = Depends(get_db)) -> dict:
    point = NavigationService(db).get_point(point_id)
    return success_response(NavigationPointResponse.model_validate(point).model_dump())


@router.get("/route", response_model=dict, summary="Get route between two points")
def get_route(origin_id: int, destination_id: int, db: Session = Depends(get_db)) -> dict:
    route: RouteResponse = NavigationService(db).get_route(origin_id, destination_id)
    return success_response(route.model_dump(), "Route calculated successfully.")
