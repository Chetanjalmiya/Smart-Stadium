"""Admin API key verification (no user login/signup required)."""
from fastapi import Header
from app.config.settings import get_settings
from app.utils.exceptions import UnauthorizedException

settings = get_settings()


def verify_admin_key(x_admin_key: str = Header(default="")) -> None:
    """Verify the X-Admin-Key header against the configured admin key."""
    if not x_admin_key or x_admin_key != settings.admin_api_key:
        raise UnauthorizedException("Invalid or missing admin API key.")
