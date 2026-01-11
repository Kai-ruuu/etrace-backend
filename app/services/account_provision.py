from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.enums import AccountRole
from app.utils.logging import Logger
from app.utils.password import hash_password
from app.models.account import Account
from app.models.system_admin_profile import SystemAdminProfile
from app.repositories.system_admin_account import SystemAdminAccountRepository
from app.repositories.system_admin_profile import SystemAdminProfileRepository

class AccountProvisionService:
    def __init__(
        self,
        db: AsyncSession,
        account_repo: SystemAdminAccountRepository,
        profile_repo: SystemAdminProfileRepository
    ) -> None:
        self.db = db
        self.account_repo = account_repo
        self.profile_repo = profile_repo
    
    async def bootstap_default_system_admin(self) -> None:
        try:
            db_system_admin = await self.account_repo.get_by_email(settings.APP_DEFAULT_SYSAD_EMAIL)
            
            if db_system_admin:
                Logger.info("Default System Administrator's account and profile already exists.")
                return
            
            hashed_password = hash_password(settings.APP_DEFAULT_SYSAD_PASS)

            account = await self.account_repo.create(Account(
                email=settings.APP_DEFAULT_SYSAD_EMAIL,
                password=hashed_password,
                role=AccountRole.SYSTEM_ADMIN,
            ))
            
            await self.profile_repo.create(SystemAdminProfile(
                account_id=account.id,
                first_name=settings.APP_DEFAULT_SYSAD_FIRST_NAME,
                last_name=settings.APP_DEFAULT_SYSAD_LAST_NAME
            ))
            
            await self.db.commit()
            
            Logger.success("Default System Administrator's account and profile has been created.")
            
        except:
            await self.db.rollback()
            Logger.error("Unable to create Default System Administrator's account and profile.")
            raise

