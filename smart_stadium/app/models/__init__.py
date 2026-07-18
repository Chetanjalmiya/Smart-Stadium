"""Import all models so they register with SQLAlchemy's Base metadata."""
from app.models.match import Match, MatchStatus
from app.models.ticket import Ticket, TicketStatus
from app.models.seat import Seat
from app.models.navigation import NavigationPoint
from app.models.crowd import CrowdDensity
from app.models.parking import ParkingSlot, ParkingBooking, ParkingSlotStatus
from app.models.food import MenuItem, FoodOrder, FoodOrderItem, OrderStatus
from app.models.weather import WeatherAlert, AlertSeverity
from app.models.sos import SOSRequest, SOSType, SOSStatus
from app.models.lost_found import LostFoundItem, LostFoundStatus, LostFoundType
from app.models.notification import Notification, NotificationCategory
from app.models.stadium_info import StadiumInfo, Amenity
from app.models.feedback import Feedback
from app.models.faq import FAQEntry, ChatLog

__all__ = [
    "Match", "MatchStatus",
    "Ticket", "TicketStatus",
    "Seat",
    "NavigationPoint",
    "CrowdDensity",
    "ParkingSlot", "ParkingBooking", "ParkingSlotStatus",
    "MenuItem", "FoodOrder", "FoodOrderItem", "OrderStatus",
    "WeatherAlert", "AlertSeverity",
    "SOSRequest", "SOSType", "SOSStatus",
    "LostFoundItem", "LostFoundStatus", "LostFoundType",
    "Notification", "NotificationCategory",
    "StadiumInfo", "Amenity",
    "Feedback",
    "FAQEntry", "ChatLog",
]
