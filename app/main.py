from fastapi import FastAPI

from app.models.all import *
from app.api import authentication
from app.api import system_admin
from app.api import school
from app.utils.setup import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(authentication.router)
app.include_router(system_admin.router)
app.include_router(school.router)