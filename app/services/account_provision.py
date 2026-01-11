from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.account import SystemAdminAccountIn, SystemAdminAccountOut
from app.core.exceptions import *
from app.core.settings import settings
from app.core.enums import Action, AccountRole
from app.utils.logging import Logger
from app.utils.password import hash_password, generate_password
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
            db_account = await self.account_repo.get_by_email(settings.APP_DEFAULT_SYSAD_EMAIL)
            
            if db_account:
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

    
    
    async def create_system_admin(self, user: Account, system_admin: SystemAdminAccountIn, as_pymodel: bool = False) -> tuple[Account, SystemAdminProfile] | SystemAdminAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_SYSTEM_ADMINS)
        
        try:
            db_account = await self.account_repo.get_by_email(system_admin.email)

            if db_account:
                raise ACCOUNT_ALREADY_EXISTS_EXCEPTION
            
            hashed_password = hash_password(generate_password())

            account = await self.account_repo.create(Account(
                email=system_admin.email,
                password=hashed_password,
                role=AccountRole.SYSTEM_ADMIN,
            ))
            
            profile = await self.profile_repo.create(SystemAdminProfile(
                account_id=account.id,
                first_name=system_admin.first_name,
                middle_name=system_admin.middle_name,
                last_name=system_admin.last_name
            ))
            
            await self.db.commit()
            await self.db.refresh(account, attribute_names=["system_admin_profile"])
            await self.db.refresh(profile)
            
            return SystemAdminAccountOut.from_account(account) if as_pymodel else (account, profile)
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to create System Administrator's account and profile - {repr(e)}")
            raise UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION

