from typing import Annotated, AsyncGenerator, Union
from jwt import decode
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import *
from app.core.settings import settings
from app.core.enums import AccountRole
from app.core.database import AsyncSessionLocal
from app.models.account import Account
from app.repositories.account import AccountRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/authentication/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(access_token: str = Cookie(None), db: AsyncSession=Depends(get_db)) -> Account:
    
    secret_key = settings.APP_JWT_AUTHENTICATION_SECRET_KEY
    secret_key_algo = settings.APP_JWT_SECRET_KEY_ALGORITHM
    
    try:
        payload = decode(access_token, secret_key, algorithms=[secret_key_algo])
        email = payload.get("sub")
        role = payload.get("role")

        if email is None or role is None:
            raise TOKEN_INVALID_CREDENTIALS_EXCEPTION
    except InvalidTokenError:
        raise TOKEN_INVALID_CREDENTIALS_EXCEPTION
    
    account_repo = AccountRepository(db, role)
    db_account = await account_repo.get_by_email(email)
    
    if not db_account:
        raise TOKEN_INVALID_CREDENTIALS_EXCEPTION
    
    if db_account.is_disabled:
        raise ACCOUNT_CURRENTLY_DISABLED_EXCEPTION

    return db_account

def allow_roles(allowed_roles: list[AccountRole]):
    def wrapper(user: Account=Depends(get_current_user)):
        user_role = user.role

        if user_role not in allowed_roles:
            raise UNAUTHORIZED_ACCESS_EXCEPION

        return user

    return wrapper

