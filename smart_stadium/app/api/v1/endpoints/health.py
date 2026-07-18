"""Health Check API endpoint."""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.config.settings import get_settings

router = APIRouter(prefix="/health", tags=["Health Check"])
settings = get_settings()


@router.get("", summary="Check API and database health")
def health_check(db: Session = Depends(get_db)) -> dict:
    """Return the health status of the API and its database connection."""
    db_status = "up"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "down"

    return {
        "success": True,
        "message": "Service is running.",
        "data": {
            "status": "healthy" if db_status == "up" else "degraded",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat(),
        },
    }
