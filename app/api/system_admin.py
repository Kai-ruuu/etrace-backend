from fastapi import Query, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.services.system_admin import SystemAdminService
from app.repositories.system_admin_account import SystemAdminAccountRepository
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles

router = APIRouter(tags=["system-admin"], prefix="/api/v1/user/system-admin")

@router.get("/search")
async def search(
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> dict:
    account_repo = SystemAdminAccountRepository(db)
    service = SystemAdminService(db, account_repo)
    return await service.search(user, query, page, page_size)

