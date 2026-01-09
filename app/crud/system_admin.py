from sqlalchemy.orm import Session

from app.exceptions import *
from app.models.all import Account, SystemAdminProfile

def get_system_admin_profile_by_id(db: Session, id: int, *, allow_none: bool=False) -> SystemAdminProfile:
    profile = db.query(SystemAdminProfile).filter(SystemAdminProfile.id == id).first()

    if not profile:
        if allow_none:
            return None
        raise PROFILE_NOT_FOUND_EXCEPTION
    
    return profile

def get_system_admin_profile_by_account_email(db: Session, account_email: str, *, allow_none: bool=False) -> SystemAdminProfile:
    profile = (
        db.query(SystemAdminProfile)
        .join(Account, Account.id == SystemAdminProfile.account_id)
        .filter(Account.email == account_email).first()
    )

    if not profile:
        if allow_none:
            return None
        raise PROFILE_NOT_FOUND_EXCEPTION
    
    return profile