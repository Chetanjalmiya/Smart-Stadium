"""API routes for the Analytics module."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.analytics_service import AnalyticsService
from app.utils.responses import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=dict, summary="Get full analytics dashboard summary")
def dashboard(db: Session = Depends(get_db)) -> dict:
    summary = AnalyticsService(db).get_dashboard_summary()
    return success_response(summary)


@router.get("/tickets", response_model=dict, summary="Get ticket analytics")
def ticket_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_ticket_analytics())


@router.get("/matches", response_model=dict, summary="Get match analytics")
def match_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_match_analytics())


@router.get("/parking", response_model=dict, summary="Get parking analytics")
def parking_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_parking_analytics())


@router.get("/food", response_model=dict, summary="Get food & beverage analytics")
def food_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_food_analytics())


@router.get("/crowd", response_model=dict, summary="Get crowd density analytics")
def crowd_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_crowd_analytics())


@router.get("/safety", response_model=dict, summary="Get safety (SOS & lost-found) analytics")
def safety_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_safety_analytics())


@router.get("/feedback", response_model=dict, summary="Get feedback analytics")
def feedback_analytics(db: Session = Depends(get_db)) -> dict:
    return success_response(AnalyticsService(db).get_feedback_analytics())
