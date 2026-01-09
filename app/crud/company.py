from sqlalchemy.orm import Session

from app.exceptions import *
from app.models.all import Account, CompanyProfile

def get_company_profile_by_id(db: Session, id: int, *, allow_none: bool=False) -> CompanyProfile:
    profile = db.query(CompanyProfile).filter(CompanyProfile.id == id).first()

    if not profile:
        if allow_none:
            return None
        raise PROFILE_NOT_FOUND_EXCEPTION
    
    return profile

def get_company_profile_by_account_email(db: Session, account_email: str, *, allow_none: bool=False) -> CompanyProfile:
    profile = (
        db.query(CompanyProfile)
        .join(Account, Account.id == CompanyProfile.account_id)
        .filter(Account.email == account_email).first()
    )

    if not profile:
        if allow_none:
            return None
        raise PROFILE_NOT_FOUND_EXCEPTION
    
    return profile

