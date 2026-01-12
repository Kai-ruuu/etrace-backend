import asyncio

from app.models.all import *
from app.services.account_provision import AccountProvisionService
from app.core.enums import AccountRole
from app.core.database import engine, AsyncSessionLocal

async def main():
    db = AsyncSessionLocal()

    try:
        admin_service = AccountProvisionService(db, AccountRole.SYSTEM_ADMIN)
        await admin_service.bootstap_default_system_admin()
    finally:
        await db.close()
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())