"""Global exception handlers registered on the FastAPI app."""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all custom exception handlers to the FastAPI application."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning("AppException on %s: %s", request.url.path, exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message, "data": None},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = [
            {"field": ".".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
            for err in exc.errors()
        ]
        logger.warning("Validation error on %s: %s", request.url.path, errors)
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": "Input validation failed.", "data": errors},
        )

    @app.exception_handler(SQLAlchemyError)
    async def db_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.error("Database error on %s: %s", request.url.path, str(exc))
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "A database error occurred.", "data": None},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled exception on %s: %s", request.url.path, str(exc))
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "An unexpected error occurred.", "data": None},
        )
