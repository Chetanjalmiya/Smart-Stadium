"""Standard API response envelope helpers."""
from typing import Any, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Consistent success response envelope."""

    success: bool = True
    message: str = "Request processed successfully."
    data: Optional[Any] = None


def success_response(data: Any = None, message: str = "Request processed successfully.") -> dict:
    """Build a standard success response dictionary."""
    return {"success": True, "message": message, "data": data}
