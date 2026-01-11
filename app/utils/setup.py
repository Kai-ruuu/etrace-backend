from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.utils.storage import initialize_storage

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_storage()
    
    yield