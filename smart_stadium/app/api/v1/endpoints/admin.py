"""Admin APIs — protected management endpoints requiring the X-Admin-Key header."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.utils.security import verify_admin_key
from app.utils.responses import success_response
from app.models.match import Match
from app.models.ticket import Ticket
from app.models.parking import ParkingSlot, ParkingBooking
from app.models.food import FoodOrder, MenuItem
from app.models.sos import SOSRequest, SOSStatus
from app.models.lost_found import LostFoundItem
from app.models.notification import Notification
from app.models.feedback import Feedback
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/admin",
    tags=["Admin APIs"],
    dependencies=[Depends(verify_admin_key)],
)


@router.get("/overview", response_model=dict, summary="Get full system overview (admin only)")
def system_overview(db: Session = Depends(get_db)) -> dict:
    overview = {
        "total_matches": db.query(Match).count(),
        "total_tickets": db.query(Ticket).count(),
        "total_parking_slots": db.query(ParkingSlot).count(),
        "active_parking_bookings": db.query(ParkingBooking).filter(ParkingBooking.is_active == 1).count(),
        "total_menu_items": db.query(MenuItem).count(),
        "total_food_orders": db.query(FoodOrder).count(),
        "open_sos_requests": db.query(SOSRequest).filter(SOSRequest.status == SOSStatus.OPEN).count(),
        "total_lost_found_items": db.query(LostFoundItem).count(),
        "total_notifications": db.query(Notification).count(),
        "average_feedback_rating": round(
            float(db.query(func.avg(Feedback.rating)).scalar() or 0.0), 2
        ),
    }
    return success_response(overview, "System overview retrieved successfully.")


@router.get("/dashboard", response_model=dict, summary="Get full analytics dashboard (admin only)")
def admin_dashboard(db: Session = Depends(get_db)) -> dict:
    summary = AnalyticsService(db).get_dashboard_summary()
    return success_response(summary, "Admin dashboard retrieved successfully.")


@router.delete("/reset-database", response_model=dict, summary="Danger: wipe all operational data (admin only)")
def reset_database(db: Session = Depends(get_db)) -> dict:
    for model in [
        Feedback, Notification, LostFoundItem, SOSRequest,
        FoodOrder, ParkingBooking, Ticket,
    ]:
        db.query(model).delete()
    db.commit()
    return success_response(None, "Operational transactional data has been reset.")
