import asyncio

from app.models.all import *
from app.services.account_provision import AccountProvisionService
from app.core.enums import AccountRole
from app.core.database import engine, AsyncSessionLocal


async def bootstrap_system_admin() -> Account:
    db = AsyncSessionLocal()

    try:
        service = AccountProvisionService(db, AccountRole.SYSTEM_ADMIN)
        return await service.bootstap_default_system_admin()
    finally:
        await db.close()
        await engine.dispose()

    
async def main():
    await bootstrap_system_admin()


if __name__ == "__main__":
    asyncio.run(main())