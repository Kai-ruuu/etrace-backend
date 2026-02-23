from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.models.all import *
from app.core.settings import settings
from app.utils.storage import paths
from app.utils.setup import lifespan
from app.utils.rate_limiting import limiter
from app.api.v1 import dean as v1_dean
from app.api.v1 import alumni as v1_alumni
from app.api.v1 import school as v1_school
from app.api.v1 import course as v1_course
from app.api.v1 import company as v1_company
from app.api.v1 import account as v1_account
from app.api.v1 import peso_staff as v1_peso_staff
from app.api.v1 import system_admin as v1_system_admin
from app.api.v1 import authentication as v1_authentication
from app.api.v1 import graduate_record as v1_graduate_record
from app.api.v1 import job_post as v1_job_post
from app.api.v1 import job_post_interest as v1_job_post_interest
from app.api.v1 import occupation as v1_occupation

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

app.include_router(v1_authentication.router)
app.include_router(v1_account.router)
app.include_router(v1_system_admin.router)
app.include_router(v1_school.router)
app.include_router(v1_dean.router)
app.include_router(v1_course.router)
app.include_router(v1_graduate_record.router)
app.include_router(v1_peso_staff.router)
app.include_router(v1_company.router)
app.include_router(v1_job_post.router)
app.include_router(v1_job_post_interest.router)
app.include_router(v1_alumni.router)
app.include_router(v1_occupation.router)

app.mount("/requirements", StaticFiles(directory=paths["company"]), name="requirements")