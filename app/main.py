from fastapi import FastAPI

from app.models.all import *
from app.api import system_admin
from app.api import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(system_admin.router)