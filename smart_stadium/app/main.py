"""Smart Stadium AI System — FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.config.logging_config import configure_logging
from app.database.init_db import init_db
from app.middleware.error_handler import register_exception_handlers
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.api.v1.router import api_router

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle handler."""
    logger.info("Starting %s v%s ...", settings.app_name, settings.app_version)
    init_db()
    logger.info("Database initialized. Application startup complete.")
    yield
    logger.info("Application shutting down.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A complete, production-ready Smart Stadium AI backend covering AI Fan Assistant, "
        "Navigation, Smart Ticketing, Live Match Info, Crowd Monitoring, Smart Parking, "
        "Food & Beverage, Weather Alerts, Emergency SOS, Lost & Found, Notifications, "
        "Seat Finder, Match Schedule, Stadium Information, Feedback, Analytics and Admin APIs."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"], summary="API root")
def root() -> dict:
    """Return basic API information and a link to the documentation."""
    return {
        "success": True,
        "message": f"Welcome to {settings.app_name} v{settings.app_version}",
        "data": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health_check": "/api/v1/health",
        },
    }
