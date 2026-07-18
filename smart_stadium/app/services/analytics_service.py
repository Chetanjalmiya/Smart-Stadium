"""Business logic for the Analytics module.

Aggregates data across other modules to provide operational insights.
"""
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.ticket import Ticket, TicketStatus
from app.models.match import Match, MatchStatus
from app.models.parking import ParkingSlot, ParkingSlotStatus
from app.models.food import FoodOrder
from app.models.crowd import CrowdDensity
from app.models.sos import SOSRequest, SOSStatus
from app.models.lost_found import LostFoundItem, LostFoundStatus
from app.models.feedback import Feedback


class AnalyticsService:
    """Encapsulates cross-module analytics and dashboard aggregation logic."""

    def __init__(self, db: Session):
        self.db = db

    def get_ticket_analytics(self) -> dict:
        total = self.db.query(Ticket).count()
        checked_in = self.db.query(Ticket).filter(Ticket.status == TicketStatus.USED).count()
        revenue = self.db.query(func.coalesce(func.sum(Ticket.price), 0.0)).scalar()
        return {
            "total_tickets_issued": total,
            "total_checked_in": checked_in,
            "check_in_rate_percent": round((checked_in / total) * 100, 2) if total else 0.0,
            "total_revenue": round(float(revenue or 0.0), 2),
        }

    def get_match_analytics(self) -> dict:
        total = self.db.query(Match).count()
        live = self.db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        completed = self.db.query(Match).filter(Match.status == MatchStatus.COMPLETED).count()
        return {"total_matches": total, "live_matches": live, "completed_matches": completed}

    def get_parking_analytics(self) -> dict:
        total = self.db.query(ParkingSlot).count()
        occupied = (
            self.db.query(ParkingSlot)
            .filter(ParkingSlot.status == ParkingSlotStatus.OCCUPIED)
            .count()
        )
        return {
            "total_slots": total,
            "occupied_slots": occupied,
            "occupancy_rate_percent": round((occupied / total) * 100, 2) if total else 0.0,
        }

    def get_food_analytics(self) -> dict:
        total_orders = self.db.query(FoodOrder).count()
        total_revenue = self.db.query(func.coalesce(func.sum(FoodOrder.total_amount), 0.0)).scalar()
        return {
            "total_orders": total_orders,
            "total_revenue": round(float(total_revenue or 0.0), 2),
        }

    def get_crowd_analytics(self) -> dict:
        avg_density = self.db.query(func.avg(CrowdDensity.density_percentage)).scalar()
        peak = self.db.query(func.max(CrowdDensity.density_percentage)).scalar()
        return {
            "average_density_percent": round(float(avg_density or 0.0), 2),
            "peak_density_percent": round(float(peak or 0.0), 2),
        }

    def get_safety_analytics(self) -> dict:
        total_sos = self.db.query(SOSRequest).count()
        open_sos = self.db.query(SOSRequest).filter(SOSRequest.status == SOSStatus.OPEN).count()
        total_lost_found = self.db.query(LostFoundItem).count()
        claimed = (
            self.db.query(LostFoundItem)
            .filter(LostFoundItem.status == LostFoundStatus.CLAIMED)
            .count()
        )
        return {
            "total_sos_requests": total_sos,
            "open_sos_requests": open_sos,
            "total_lost_found_reports": total_lost_found,
            "claimed_items": claimed,
        }

    def get_feedback_analytics(self) -> dict:
        avg_rating = self.db.query(func.avg(Feedback.rating)).scalar()
        total = self.db.query(Feedback).count()
        return {"average_rating": round(float(avg_rating or 0.0), 2), "total_feedback": total}

    def get_dashboard_summary(self) -> dict:
        return {
            "tickets": self.get_ticket_analytics(),
            "matches": self.get_match_analytics(),
            "parking": self.get_parking_analytics(),
            "food": self.get_food_analytics(),
            "crowd": self.get_crowd_analytics(),
            "safety": self.get_safety_analytics(),
            "feedback": self.get_feedback_analytics(),
        }
