from datetime import datetime, timezone, timedelta

from app.core.settings import settings

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

def get_access_token_expiry() -> datetime:
    expiry_delta = timedelta(minutes=settings.APP_ACCESS_TOKEN_EXPIRY_MINUTES)
    return datetime.now(timezone.utc) + expiry_delta

