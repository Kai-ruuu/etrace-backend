from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, literal

from app.core.enums import AccountRole
from app.schemas.system_admin_profile import SystemAdminProfileOut
from app.models.account import Account
from app.models.system_admin_profile import SystemAdminProfile

class SystemAdminProfileRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def create(self, profile: SystemAdminProfile) -> SystemAdminProfile:
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile
    
    async def get_by_id(self, id: int, as_pymodel: bool = False) -> SystemAdminProfile | SystemAdminProfileOut | None:
        statement = (
            select(SystemAdminProfile)
            .join(Account, Account.id == SystemAdminProfile.account_id)
            .where(
                SystemAdminProfile.id == id,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        profile = result.scalar_one_or_none()

        if not profile:
            return None
        
        return SystemAdminProfileOut.model_validate(profile) if as_pymodel else profile
    
    async def get_by_account_id(self, account_id: int, as_pymodel: bool = False) -> SystemAdminProfile | SystemAdminProfileOut | None:
        statement = (
            select(SystemAdminProfile)
            .join(Account, Account.id == SystemAdminProfile.account_id)
            .where(
                SystemAdminProfile.account_id == account_id,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        profile = result.scalar_one_or_none()

        if not profile:
            return None
        
        return SystemAdminProfileOut.model_validate(profile) if as_pymodel else profile
    