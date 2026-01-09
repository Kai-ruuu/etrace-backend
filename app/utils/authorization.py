from typing import Annotated
from sqlalchemy.orm import Session
from jwt import decode
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.exceptions import *
from app.utils.env import envs
from app.database import get_db
from app.models.all import Account
from app.enums.all import AccountRole
from app.crud.account import get_account_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/authentication/login")

def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)], db: Session=Depends(get_db)) -> Account:
    secret_key = envs("APP_DB_URL")
    secret_key_algo = envs("APP_JWT_SECRET_KEY_ALGORITHM")
    
    try:
        payload = decode(access_token, secret_key, algorithms=[secret_key_algo])
        email = payload.get("sub")

        # raise if emails is missing
        if email is None:
            raise TOKEN_INVALID_CREDENTIALS_EXCEPTION
    except InvalidTokenError:
        raise TOKEN_INVALID_CREDENTIALS_EXCEPTION
    
    user_account = get_account_by_email(
        db=db,
        email=email,
        allow_none=True,
    )
    
    # raise if user's account is not recognized
    if not user_account:
        raise TOKEN_INVALID_CREDENTIALS_EXCEPTION
    
    # raise if users's account is disabled
    if user_account.is_disabled:
        raise ACCOUNT_CURRENTLY_DISABLED_EXCEPTION

    return user_account

def allow_roles(allowed_roles: list[AccountRole]):
    def wrapper(user: Account=Depends(get_current_user)):
        user_role = user.role

        if user_role not in allowed_roles:
            raise UNAUTHORIZED_ACCESS_EXCEPTION

        return user

    return wrapper

