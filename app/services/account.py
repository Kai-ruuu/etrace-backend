from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import *
from app.core.enums import AccountRole
from app.models.account import Account
from app.utils.password import verify_password
from app.schemas.account import ChangePasswordIn
from app.repositories.account import AccountRepository
from app.schemas.account import (
    SystemAdminAccountOut,
    DeanAccountOut,
    PesoStaffAccountOut,
    CompanyAccountOut,
    AlumniAccountOut
)


class AccountService:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db
        self.role = role
        self.account_repo = AccountRepository(self.db, role)
        
    
    async def change_password(self, user: Account, change_password_info: ChangePasswordIn, as_pymodel: bool = False) -> (
        Account |
        SystemAdminAccountOut |
        DeanAccountOut |
        PesoStaffAccountOut |
        CompanyAccountOut |
        AlumniAccountOut
    ):
        if user.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if not verify_password(change_password_info.old_password, user.password):
            raise ACCOUNT_CHANGE_PASSWORD_INCORRECT_EXCEPTION
        
        updated_db_account = await self.account_repo.change_password(user, change_password_info.new_password)
        return self.AccountProfilePymodel.model_validate(updated_db_account) if as_pymodel else updated_db_account

    
    @property
    def AccountProfilePymodel(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return SystemAdminAccountOut
            case AccountRole.PESO_STAFF: return PesoStaffAccountOut
            case AccountRole.COMPANY: return CompanyAccountOut
            case AccountRole.ALUMNI: return AlumniAccountOut
            case AccountRole.DEAN: return DeanAccountOut
            case _: raise ValueError("Invalid role value.")
        

# continue on:
# [x] password change feature
# [x] profile management feature