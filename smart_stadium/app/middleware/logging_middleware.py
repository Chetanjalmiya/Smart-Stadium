"""HTTP request/response logging middleware."""
import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every incoming HTTP request with timing and a correlation id."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        logger.info(
            "[%s] --> %s %s", request_id, request.method, request.url.path
        )

        response = await call_next(request)

        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            "[%s] <-- %s %s status=%s duration=%sms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response
