"""Business logic for the Weather Alerts module."""
from typing import List
from sqlalchemy.orm import Session
from app.models.weather import WeatherAlert
from app.schemas.weather import WeatherAlertCreate
from app.utils.exceptions import NotFoundException


class WeatherService:
    """Encapsulates weather alert creation and retrieval logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_alert(self, payload: WeatherAlertCreate) -> WeatherAlert:
        alert = WeatherAlert(**payload.model_dump())
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def list_alerts(self, active_only: bool = False) -> List[WeatherAlert]:
        query = self.db.query(WeatherAlert)
        if active_only:
            query = query.filter(WeatherAlert.is_active == 1)
        return query.order_by(WeatherAlert.issued_at.desc()).all()

    def get_alert(self, alert_id: int) -> WeatherAlert:
        alert = self.db.query(WeatherAlert).filter(WeatherAlert.id == alert_id).first()
        if not alert:
            raise NotFoundException("Weather alert", alert_id)
        return alert

    def deactivate_alert(self, alert_id: int) -> WeatherAlert:
        alert = self.get_alert(alert_id)
        alert.is_active = 0
        self.db.commit()
        self.db.refresh(alert)
        return alert
