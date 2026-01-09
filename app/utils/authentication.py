from jwt import encode
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions import *
from app.schemas.access_token import Token
from app.crud.account import get_account_by_email
from app.utils.password import verify_password
from app.utils.env import envs
from app.utils.datetime import get_access_token_expiry

def create_access_token(data: dict) -> str:
    expiry = get_access_token_expiry()
    secret_key = envs("APP_DB_URL")
    secret_key_algo = envs("APP_JWT_SECRET_KEY_ALGORITHM")
    data.update({"exp": expiry})

    return encode(data, secret_key, secret_key_algo)

def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm) -> Token:
    db_account = get_account_by_email(db=db, email=form_data.username)

    if not db_account or not verify_password(form_data.password, db_account.password):
        raise AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION
    
    return Token(
        access_token=create_access_token(data={"sub": db_account.email}),
        token_type="bearer"
    )

