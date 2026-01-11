from jwt import encode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.models.account import Account
from app.schemas.authentication import Token
from app.core.exceptions import *
from app.core.settings import settings
from app.utils.password import verify_password
from app.utils.datetime import get_access_token_expiry


class AuthenticationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def create_access_token(self, data: dict) -> str:
        expiry = get_access_token_expiry()
        secret_key = settings.APP_JWT_AUTHENTICATION_SECRET_KEY
        secret_key_algo = settings.APP_JWT_SECRET_KEY_ALGORITHM
        data.update({"exp": expiry})
        return encode(data, secret_key, secret_key_algo)

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> Token:
        statement = select(Account).where(Account.email == form_data.username)
        result = await self.db.execute(statement)
        db_account = result.scalar_one_or_none()
        
        if not db_account:
            raise AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION
        
        if not verify_password(form_data.password, db_account.password):
            raise AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION
        
        if db_account.is_disabled:
            raise ACCOUNT_CURRENTLY_DISABLED_EXCEPTION
        
        access_token = self.create_access_token(data={"sub": db_account.email})
        
        return Token(
            access_token=access_token,
            token_type="bearer"
        )