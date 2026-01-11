from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, literal

from app.core.enums import AccountRole
from app.schemas.account import SystemAdminAccountOut
from app.models.account import Account
from app.models.system_admin_profile import SystemAdminProfile

class SystemAdminAccountRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def create(self, account: Account) -> Account:
        self.db.add(account)
        await self.db.flush()
        await self.db.refresh(account)
        return account
    
    async def get_by_id(self, id: int, as_pymodel: bool = False) -> Account | SystemAdminAccountOut | None:
        statement = (
            select(Account)
            .options(selectinload(Account.system_admin_profile))
            .where(
                Account.id == id,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        account = result.scalar_one_or_none()

        if not account:
            return None
        
        return SystemAdminAccountOut.model_validate(account) if as_pymodel else account
    
    async def get_by_email(self, email: str, as_pymodel: bool = False) -> Account | SystemAdminAccountOut | None:
        statement = (
            select(Account)
            .options(selectinload(Account.system_admin_profile))
            .where(
                Account.email == email,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        account = result.scalar_one_or_none()

        if not account:
            return None
        
        return SystemAdminAccountOut.model_validate(account) if as_pymodel else account
    
    async def disable_by_id(self, account: Account, as_pymodel: bool = False) -> Account | SystemAdminAccountOut:
        account.is_disabled = True
        self.db.commit()
        self.db.refresh(account, attribute_names=["system_admin_profile"])
        return SystemAdminAccountOut.model_validate(account) if as_pymodel else account
    
    async def enable_by_id(self, account: Account, as_pymodel: bool = False) -> Account | SystemAdminAccountOut:
        account.is_disabled = False
        self.db.commit()
        self.db.refresh(account, attribute_names=["system_admin_profile"])
        return SystemAdminAccountOut.model_validate(account) if as_pymodel else account
    
    async def search(
        self,
        query: str | None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        base_statement = (
            select(Account)
            .options(selectinload(Account.system_admin_profile))
            .join(SystemAdminProfile)
            .where(Account.role == AccountRole.SYSTEM_ADMIN)
        )

        count_statement = (
            select(func.count())
            .select_from(Account)
            .join(SystemAdminProfile)
            .where(Account.role == AccountRole.SYSTEM_ADMIN)
        )

        if query:
            search_filter = or_(
                Account.email.ilike(f"%{query}%"),
                SystemAdminProfile.first_name.ilike(f"%{query}%"),
                func.coalesce(SystemAdminProfile.middle_name, literal("")).ilike(f"%{query}%"),
                SystemAdminProfile.last_name.ilike(f"%{query}%"),
            )
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)

        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size

        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        accounts = result.scalars().unique().all()

        items = [SystemAdminAccountOut.from_account(account) for account in accounts]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

