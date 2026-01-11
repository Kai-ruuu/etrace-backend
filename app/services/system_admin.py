from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import *
from app.core.enums import Action
from app.schemas.account import SystemAdminAccountOut
from app.models.account import Account
from app.repositories.system_admin_account import SystemAdminAccountRepository

class SystemAdminService:
    def __init__(
        self,
        db: AsyncSession,
        account_repo: SystemAdminAccountRepository
    ) -> None:
        self.db = db
        self.account_repo = account_repo

    async def get_by_id(
        self,
        user: Account,
        id: int,
        as_pymodel: bool = False
    ) -> Account | SystemAdminAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_SYSTEM_ADMINS)
        
        db_profile = await self.account_repo.get_by_id(id, as_pymodel)

        if not db_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
        
        return db_profile

    async def get_by_email(
        self,
        user: Account,
        email: str,
        as_pymodel: bool = False
    ) -> Account | SystemAdminAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_SYSTEM_ADMINS)
        
        db_profile = await self.account_repo.get_by_email(email, as_pymodel)

        if not db_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
        
        return db_profile

    async def search(
        self,
        user: Account,
        query: int,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_SYSTEM_ADMINS)
        
        return await self.account_repo.search(query, page, page_size)
    
    