from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import *
from app.core.enums import Action
from app.core.enums import AccountRole
from app.models.account import Account
from app.schemas.account import DeanAccountOut
from app.repositories.account import AccountRepository


class DeanService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.account_repo = AccountRepository(self.db, AccountRole.DEAN)
    

    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | DeanAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_DEANS)
        
        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        return DeanAccountOut.model_validate(db_account) if as_pymodel else db_account
        

    async def get_by_email(self, user: Account, email: str, as_pymodel: bool = False) -> Account | DeanAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_DEANS)
        
        db_account = await self.account_repo.get_by_email(email)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        return DeanAccountOut.model_validate(db_account) if as_pymodel else db_account
        

    async def search(self, user: Account, query: str, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_DEANS)
        
        accounts, total, total_pages = await self.account_repo.search(query, page, page_size)

        items = [DeanAccountOut.model_validate(account) for account in accounts]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    

    async def disable_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | DeanAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ENABLE_DISABLE_PESO_STAFFS)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if db_account.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if db_account.is_disabled:
            raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
        
        db_account = await self.account_repo.disable(db_account)

        return DeanAccountOut.model_validate(db_account) if as_pymodel else db_account


    
    async def enable_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | DeanAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ENABLE_DISABLE_PESO_STAFFS)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION

        if db_account.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if not db_account.is_disabled:
            raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
        
        db_account = await self.account_repo.enable(db_account)
    
        return DeanAccountOut.model_validate(db_account) if as_pymodel else db_account


