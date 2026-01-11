from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_db
from app.schemas.authentication import Token
from app.services.authentication import AuthenticationService

router = APIRouter(tags=["all"], prefix="/api/v1/authentication")

@router.post("/login", response_model=Token, tags=["tested"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_db)) -> Token:
    authentication_service = AuthenticationService(db)
    return await authentication_service.authenticate_user(form_data)

