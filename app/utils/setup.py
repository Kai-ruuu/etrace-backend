from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from app.models.all import *
from app.utils.env import envs
from app.database import get_db
from app.database import Base, engine
from app.enums.all import AccountRole
from app.utils.password import hash_password
from app.utils.storage import initialize_storage
from app.crud.account import get_account_by_email
from app.crud.system_admin import get_system_admin_profile_by_account_email

def bootstrap_default_system_admin() -> None:
    
    DEFAULT_SYSAD_EMAIL = envs("DEFAULT_SYSAD_EMAIL")
    DEFAULT_SYSAD_PASSWORD = envs("DEFAULT_SYSAD_PASSWORD")
    DEFAULT_SYSAD_FIRST_NAME = envs("DEFAULT_SYSAD_FIRST_NAME")
    DEFAULT_SYSAD_LAST_NAME = envs("DEFAULT_SYSAD_LAST_NAME")
    
    if not all((DEFAULT_SYSAD_EMAIL, DEFAULT_SYSAD_PASSWORD, DEFAULT_SYSAD_FIRST_NAME, DEFAULT_SYSAD_LAST_NAME)):
        raise RuntimeError("[SETUP] Default System Administrator's credentials must be set within the environment variables.")
    
    db: Session = next(get_db())

    try:
        account = get_account_by_email(db, email=DEFAULT_SYSAD_EMAIL, allow_none=True)
        profile = get_system_admin_profile_by_account_email(db, account_email=DEFAULT_SYSAD_EMAIL, allow_none=True)
        
        if account and profile:
            print("[SETUP] Default System Administrator's account and profile already exists.")
            return
        
        account = Account(
            role=AccountRole.SYSTEM_ADMINISTRATOR,
            email=DEFAULT_SYSAD_EMAIL,
            password=hash_password(DEFAULT_SYSAD_PASSWORD),
        )
        db.add(account)
        db.flush()

        profile = SystemAdminProfile(
            first_name=DEFAULT_SYSAD_FIRST_NAME,
            last_name=DEFAULT_SYSAD_LAST_NAME,
            account_id=account.id
        )
        db.add(profile)
        db.commit()
        print("[SETUP] Default System Administrator's account and profile has been created.")
    finally:
        db.close()

@asynccontextmanager
async def app_setup(app: FastAPI):
    initialize_storage()
    Base.metadata.create_all(bind=engine)
    bootstrap_default_system_admin()
    yield

