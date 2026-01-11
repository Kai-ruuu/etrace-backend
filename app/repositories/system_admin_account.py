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
        
    
    async def get_by_id(self, id: int) -> Account | None:
        statement = (
            select(Account)
            .options(selectinload(Account.system_admin_profile))
            .where(
                Account.id == id,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
        
        
    async def get_by_email(self, email: str) -> Account | None:
        statement = (
            select(Account)
            .options(selectinload(Account.system_admin_profile))
            .where(
                Account.email == email,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    
    
    async def disable(self, db_account: Account) -> Account:
        db_account.is_disabled = True

        await self.db.commit()
        await self.db.refresh(db_account, attribute_names=["system_admin_profile"])
        return db_account
    
    
    async def enable(self, db_account: Account) -> Account:
        db_account.is_disabled = False

        await self.db.commit()
        await self.db.refresh(db_account, attribute_names=["system_admin_profile"])
        return db_account
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[Account], int, int]:
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

        return accounts, total, total_pages

        

