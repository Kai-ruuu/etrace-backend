from jwt import encode
from fastapi import Response
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.core.enums import AccountRole
from app.core.settings import settings
from app.repositories.account import AccountRepository
from app.services.external.geocoding import GeocodingService
from app.schemas.account import (
    CompanyAccountOut,
    AlumniAccountOut,
    DeanAccountOut,
    PesoStaffAccountOut,
    SystemAdminAccountOut
)
from app.schemas.authentication import LoginCredentials
from app.core.exceptions import *
from app.core.settings import settings
from app.utils.password import verify_password
from app.utils.datetime import get_access_token_expiry


class AuthenticationService(GeocodingService):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        
        self.db = db
        
    
    def AccountPymodel(self, user: Account) -> (
        SystemAdminAccountOut |
        PesoStaffAccountOut |
        CompanyAccountOut |
        AlumniAccountOut |
        DeanAccountOut
    ):
        match user.role:
            case AccountRole.SYSTEM_ADMIN: return SystemAdminAccountOut
            case AccountRole.PESO_STAFF: return PesoStaffAccountOut
            case AccountRole.COMPANY: return CompanyAccountOut
            case AccountRole.ALUMNI: return AlumniAccountOut
            case AccountRole.DEAN: return DeanAccountOut
            case _:
                raise ValueError("Invalid role value.")
            
    
    def add_required_info(self, user_info: SystemAdminAccountOut | PesoStaffAccountOut | CompanyAccountOut | AlumniAccountOut | DeanAccountOut) -> dict:
        if user_info.get("role") == AccountRole.ALUMNI:
            location_info = self.geocode(user_info["alumni_profile"]["address"])
            user_info["alumni_profile"]["location_info"] = location_info
        
        return user_info


    def create_access_token(self, data: dict) -> tuple[str, datetime]:
        expiry = get_access_token_expiry()
        secret_key = settings.APP_JWT_AUTHENTICATION_SECRET_KEY
        secret_key_algo = settings.APP_JWT_SECRET_KEY_ALGORITHM
        data.update({"exp": expiry})
        return encode(data, secret_key, secret_key_algo), expiry


    async def login(self, response: Response, form_data: LoginCredentials):
        statement = select(Account).where(Account.email == form_data.email)
        result = await self.db.execute(statement)
        db_account = result.scalar_one_or_none()
        
        if not db_account:
            raise AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION
        
        if not verify_password(form_data.password, db_account.password):
            raise AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION
        
        if db_account.is_disabled:
            raise ACCOUNT_CURRENTLY_DISABLED_EXCEPTION
        
        account_repo = AccountRepository(self.db, db_account.role)
        access_token, exp_datetime = self.create_access_token({
            "sub": db_account.email,
            "role": db_account.role
        })
        exp_timestamp = int(exp_datetime.timestamp())
        
        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly = True,
            secure = False,
            samesite = "lax",
            expires = exp_timestamp,
            max_age = 60 * settings.APP_ACCESS_TOKEN_EXPIRY_MINUTES,
        )
        
        user = await account_repo.get_by_email(db_account.email)
        user_info = self.AccountPymodel(user).model_validate(user).model_dump()
        return self.add_required_info(user_info)
    
    
    def logout(self, response: Response):
        response.delete_cookie("access_token")
        return {"detail": "Logged out successfully."}
    

    def current_user_to_pymodel(self, user: Account):
        user_info = self.AccountPymodel(user).model_validate(user).model_dump()
        return self.add_required_info(user_info)