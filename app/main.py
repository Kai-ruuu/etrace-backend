from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.all import *
from app.core.settings import settings
from app.utils.setup import lifespan
from app.utils.rate_limiting import limiter
from app.api import dean
from app.api import alumni
from app.api import school
from app.api import course
from app.api import company
from app.api import account
from app.api import peso_staff
from app.api import system_admin
from app.api import authentication
from app.api import graduate_record
from app.api import job_post
from app.api import job_post_interest

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True,
    allow_origins = [settings.APP_FRONTEND_URL],
)

app.include_router(authentication.router)
app.include_router(account.router)
app.include_router(system_admin.router)
app.include_router(school.router)
app.include_router(dean.router)
app.include_router(course.router)
app.include_router(graduate_record.router)
app.include_router(peso_staff.router)
app.include_router(company.router)
app.include_router(job_post.router)
app.include_router(job_post_interest.router)
app.include_router(alumni.router)