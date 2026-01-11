import asyncio

from app.core.database import engine, AsyncSessionLocal
from app.models.all import *
from app.services.account_provision import AccountProvisionService
from app.repositories.system_admin_account import SystemAdminAccountRepository
from app.repositories.system_admin_profile import SystemAdminProfileRepository

async def main():
    db = AsyncSessionLocal()

    try:
        account_repo = SystemAdminAccountRepository(db)
        profile_repo = SystemAdminProfileRepository(db)
        admin_service = AccountProvisionService(db, account_repo, profile_repo)
        await admin_service.bootstap_default_system_admin()
    finally:
        await db.close()
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())