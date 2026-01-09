from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.routers import system_admin
from app.routers import authentication
from app.utils.api import limiter
from app.utils.setup import app_setup

app = FastAPI(lifespan=app_setup)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(authentication.router)
app.include_router(system_admin.router)

