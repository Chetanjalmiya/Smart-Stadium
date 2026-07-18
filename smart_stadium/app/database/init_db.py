"""Database table creation and initial seed data for the Smart Stadium system."""
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.base import Base, engine, SessionLocal
import app.models  # noqa: F401  (ensures all models are registered on Base.metadata)
from app.models.match import Match, MatchStatus
from app.models.seat import Seat
from app.models.navigation import NavigationPoint
from app.models.parking import ParkingSlot
from app.models.food import MenuItem
from app.models.stadium_info import StadiumInfo, Amenity
from app.models.faq import FAQEntry

logger = logging.getLogger(__name__)


def create_tables() -> None:
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified successfully.")


def seed_data() -> None:
    """Populate the database with initial reference data, if not already present."""
    db: Session = SessionLocal()
    try:
        if db.query(Match).count() == 0:
            now = datetime.utcnow()
            db.add_all([
                Match(
                    home_team="Falcons FC",
                    away_team="Eagles United",
                    venue="Main Arena",
                    scheduled_time=now + timedelta(days=2),
                    status=MatchStatus.SCHEDULED,
                ),
                Match(
                    home_team="Titans SC",
                    away_team="Warriors FC",
                    venue="Main Arena",
                    scheduled_time=now - timedelta(minutes=30),
                    status=MatchStatus.LIVE,
                    home_score=1,
                    away_score=0,
                    current_minute=35,
                ),
            ])

        if db.query(Seat).count() == 0:
            for section in ["A", "B", "C"]:
                for row in range(1, 4):
                    for num in range(1, 6):
                        db.add(Seat(
                            seat_number=f"{section}{row}-{num}",
                            section=f"Section {section}",
                            row=str(row),
                            gate=f"Gate {section}",
                            is_accessible=(num == 1),
                            category="premium" if section == "A" else "general",
                        ))

        if db.query(NavigationPoint).count() == 0:
            db.add_all([
                NavigationPoint(name="Main Entrance", category="entrance", zone="North", pos_x=0, pos_y=0, description="Primary stadium entrance."),
                NavigationPoint(name="Gate A", category="gate", zone="North", pos_x=10, pos_y=5, description="Entry gate for Section A."),
                NavigationPoint(name="Gate B", category="gate", zone="East", pos_x=50, pos_y=20, description="Entry gate for Section B."),
                NavigationPoint(name="Restroom - North", category="restroom", zone="North", pos_x=15, pos_y=10, description="North wing restrooms."),
                NavigationPoint(name="Food Court", category="food", zone="Central", pos_x=30, pos_y=30, description="Main food and beverage court."),
                NavigationPoint(name="First Aid Station", category="medical", zone="Central", pos_x=25, pos_y=25, description="Medical assistance point."),
                NavigationPoint(name="Parking Zone P1", category="parking", zone="South", pos_x=5, pos_y=60, description="Main visitor parking zone."),
            ])

        if db.query(ParkingSlot).count() == 0:
            for zone in ["P1", "P2"]:
                for i in range(1, 11):
                    db.add(ParkingSlot(
                        slot_number=f"{zone}-{i:02d}",
                        zone=zone,
                        vehicle_type="car",
                        hourly_rate=5.0,
                    ))

        if db.query(MenuItem).count() == 0:
            db.add_all([
                MenuItem(name="Stadium Burger", category="Main Course", price=8.5, stall_location="Stall 1", description="Classic beef burger with cheese."),
                MenuItem(name="Loaded Nachos", category="Snacks", price=6.0, stall_location="Stall 2", description="Nachos with cheese and jalapenos."),
                MenuItem(name="Cola (500ml)", category="Beverages", price=3.0, stall_location="Stall 1", description="Chilled soft drink."),
                MenuItem(name="Veggie Wrap", category="Main Course", price=7.0, stall_location="Stall 3", description="Grilled vegetable wrap."),
                MenuItem(name="Popcorn", category="Snacks", price=4.5, stall_location="Stall 2", description="Salted popcorn bucket."),
            ])

        if db.query(StadiumInfo).count() == 0:
            db.add_all([
                StadiumInfo(key="hours", title="Stadium Operating Hours", content="The stadium opens 3 hours before kickoff and closes 2 hours after the event ends."),
                StadiumInfo(key="rules", title="Stadium Rules", content="No outside food or drinks. No smoking except in designated areas. Bags larger than A4 size are not permitted."),
                StadiumInfo(key="contact", title="Contact & Support", content="For assistance, visit any information desk or call the stadium helpline at +1-800-555-0199."),
            ])

        if db.query(Amenity).count() == 0:
            db.add_all([
                Amenity(name="North Restroom", category="restroom", location="North Wing, Level 1", description="Accessible restrooms available."),
                Amenity(name="Fan Store", category="retail", location="Main Concourse", description="Official team merchandise."),
                Amenity(name="ATM", category="services", location="Near Gate B", description="24/7 cash withdrawal."),
                Amenity(name="Prayer Room", category="services", location="South Wing, Level 1", description="Quiet room for prayer/meditation."),
            ])

        if db.query(FAQEntry).count() == 0:
            db.add_all([
                FAQEntry(
                    keywords="parking cost price fee",
                    question="How much does parking cost?",
                    answer="Parking costs $5 per hour. You can book a slot via the Smart Parking module.",
                    category="parking",
                ),
                FAQEntry(
                    keywords="food menu eat drink beverage",
                    question="What food is available?",
                    answer="We offer burgers, wraps, nachos, popcorn and beverages at multiple stalls. Check the Food & Beverage menu for the full list.",
                    category="food",
                ),
                FAQEntry(
                    keywords="ticket qr entry gate check in",
                    question="How do I check in with my ticket?",
                    answer="Show your QR code ticket at any gate scanner, or use the /tickets/verify API to check in.",
                    category="ticket",
                ),
                FAQEntry(
                    keywords="lost item found belongings",
                    question="I lost an item, what do I do?",
                    answer="Report it through the Lost & Found module with a description and your contact details, and our staff will help locate it.",
                    category="lost_found",
                ),
                FAQEntry(
                    keywords="emergency help medical sos safety",
                    question="What do I do in an emergency?",
                    answer="Use the Emergency SOS feature immediately with your location. Our safety team will respond right away.",
                    category="safety",
                ),
                FAQEntry(
                    keywords="restroom toilet washroom bathroom",
                    question="Where is the nearest restroom?",
                    answer="Restrooms are located in the North and South wings on every level. Use Stadium Navigation to find the nearest one.",
                    category="navigation",
                ),
            ])

        db.commit()
        logger.info("Seed data inserted successfully (or already present).")
    finally:
        db.close()


def init_db() -> None:
    """Initialize the database: create tables and seed baseline data."""
    create_tables()
    seed_data()
