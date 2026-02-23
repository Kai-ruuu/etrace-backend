from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.utils.storage import initialize_storage

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_storage()
    # [debug]
    # print("\n=== Registered Routes ===")
    # for route in app.routes:
    #     if hasattr(route, 'methods'):
    #         print(f"{route.methods} {route.path}")
    # print("========================\n")
    yield