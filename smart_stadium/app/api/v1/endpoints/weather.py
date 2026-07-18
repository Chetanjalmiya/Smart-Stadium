"""API routes for the Weather Alerts module."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.weather_service import WeatherService
from app.schemas.weather import WeatherAlertCreate, WeatherAlertResponse
from app.utils.responses import success_response

router = APIRouter(prefix="/weather", tags=["Weather Alerts"])


@router.post("", response_model=dict, status_code=201, summary="Issue a weather alert")
def create_alert(payload: WeatherAlertCreate, db: Session = Depends(get_db)) -> dict:
    alert = WeatherService(db).create_alert(payload)
    return success_response(WeatherAlertResponse.model_validate(alert).model_dump(), "Weather alert issued.")


@router.get("", response_model=dict, summary="List weather alerts")
def list_alerts(active_only: bool = Query(default=False), db: Session = Depends(get_db)) -> dict:
    alerts = WeatherService(db).list_alerts(active_only)
    data = [WeatherAlertResponse.model_validate(a).model_dump() for a in alerts]
    return success_response(data, f"Retrieved {len(data)} weather alert(s).")


@router.get("/{alert_id}", response_model=dict, summary="Get weather alert by ID")
def get_alert(alert_id: int, db: Session = Depends(get_db)) -> dict:
    alert = WeatherService(db).get_alert(alert_id)
    return success_response(WeatherAlertResponse.model_validate(alert).model_dump())


@router.post("/{alert_id}/deactivate", response_model=dict, summary="Deactivate a weather alert")
def deactivate_alert(alert_id: int, db: Session = Depends(get_db)) -> dict:
    alert = WeatherService(db).deactivate_alert(alert_id)
    return success_response(WeatherAlertResponse.model_validate(alert).model_dump(), "Weather alert deactivated.")
