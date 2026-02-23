from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.schemas.account import CompanyAccountOut
from app.repositories.account import AccountRepository
from app.repositories.profile import ProfileRepository
from app.core.exceptions import *
from app.core.enums import AccountRole, Action, CompanyApprovalStatus


class CompanyService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.account_repo = AccountRepository(self.db, AccountRole.COMPANY)
        self.profile_repo = ProfileRepository(self.db, AccountRole.COMPANY)
    

    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COMPANIES)
        
        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account
        

    async def get_by_email(self, user: Account, email: str, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COMPANIES)
        
        db_account = await self.account_repo.get_by_email(email)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account
        

    async def search(self, user: Account, query: str, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COMPANIES)
        
        accounts, total, total_pages = await self.account_repo.search(query, page, page_size)

        items = [CompanyAccountOut.model_validate(account) for account in accounts]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    

    async def disable_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ENABLE_DISABLE_COMPANIES)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if db_account.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if db_account.is_disabled:
            raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
        
        db_account = await self.account_repo.disable(db_account)

        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account


    
    async def enable_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ENABLE_DISABLE_COMPANIES)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION

        if db_account.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if not db_account.is_disabled:
            raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
        
        db_account = await self.account_repo.enable(db_account)
    
        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def approve_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.APPROVE_COMPANIES)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if user.role == AccountRole.SYSTEM_ADMIN:
            if db_account.company_profile.sysad_approval_status == CompanyApprovalStatus.APPROVED:
                raise COMPANY_ALREADY_APPROVED_EXCEPTION

            await self.profile_repo.approve_company_as_system_admin_by_account_id(id)
        else:
            if db_account.company_profile.peso_staff_approval_status == CompanyApprovalStatus.APPROVED:
                raise COMPANY_ALREADY_APPROVED_EXCEPTION

            await self.profile_repo.approve_company_as_peso_staff_by_account_id(id)
        
        db_account = await self.account_repo.get_by_id(id)

        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def reject_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.REJECT_COMPANIES)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if user.role == AccountRole.SYSTEM_ADMIN:
            if db_account.company_profile.sysad_approval_status == CompanyApprovalStatus.REJECTED:
                raise COMPANY_ALREADY_REJECTED_EXCEPTION

            await self.profile_repo.reject_company_as_system_admin_by_account_id(id)
        else:
            if db_account.company_profile.peso_staff_approval_status == CompanyApprovalStatus.REJECTED:
                raise COMPANY_ALREADY_REJECTED_EXCEPTION
            
            await self.profile_repo.reject_company_as_peso_staff_by_account_id(id)
        
        db_account = await self.account_repo.get_by_id(id)

        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def pend_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | CompanyAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.PEND_COMPANIES)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if user.role == AccountRole.SYSTEM_ADMIN:
            if db_account.company_profile.sysad_approval_status == CompanyApprovalStatus.PENDING:
                raise COMPANY_ALREADY_PENDING_EXCEPTION

            await self.profile_repo.pend_company_as_system_admin_by_account_id(id)
        else:
            if db_account.company_profile.peso_staff_approval_status == CompanyApprovalStatus.PENDING:
                raise COMPANY_ALREADY_PENDING_EXCEPTION
            
            await self.profile_repo.pend_company_as_peso_staff_by_account_id(id)
        
        db_account = await self.account_repo.get_by_id(id)

        return CompanyAccountOut.model_validate(db_account) if as_pymodel else db_account


