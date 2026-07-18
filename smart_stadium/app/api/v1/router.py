"""Aggregates all v1 API routers into a single APIRouter."""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    matches,
    tickets,
    seats,
    navigation,
    crowd,
    parking,
    food,
    weather,
    sos,
    lost_found,
    notifications,
    stadium_info,
    feedback,
    assistant,
    analytics,
    admin,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(assistant.router)
api_router.include_router(navigation.router)
api_router.include_router(tickets.router)
api_router.include_router(matches.router)
api_router.include_router(crowd.router)
api_router.include_router(parking.router)
api_router.include_router(food.router)
api_router.include_router(weather.router)
api_router.include_router(sos.router)
api_router.include_router(lost_found.router)
api_router.include_router(notifications.router)
api_router.include_router(seats.router)
api_router.include_router(stadium_info.router)
api_router.include_router(feedback.router)
api_router.include_router(analytics.router)
api_router.include_router(admin.router)
