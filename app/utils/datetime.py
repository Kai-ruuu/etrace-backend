from datetime import datetime, timezone, timedelta

from app.utils.env import envi

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

def get_access_token_expiry() -> datetime:
    expiry_delta = timedelta(minutes=envi("APP_ACCESS_TOKEN_EXPIRY_MINUTES"))
    return datetime.now(timezone.utc) + expiry_delta

