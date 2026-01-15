from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Query, Depends, APIRouter

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.schemas.account import SystemAdminAccountIn, SystemAdminAccountOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.services.system_admin import SystemAdminService
from app.services.account_provision import AccountProvisionService


router = APIRouter(tags=["system-admin"], prefix="/api/v1/user/system-admin")


@router.post("/", response_model=SystemAdminAccountOut, tags=["system-admin: tested"])
@limiter.limit("10/minute")
async def create(
    request: Request,
    system_admin: SystemAdminAccountIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> SystemAdminAccountOut:
    service = AccountProvisionService(db, AccountRole.SYSTEM_ADMIN)
    return await service.create_system_admin(user, system_admin, True)
    

@router.get("/search", tags=["system-admin: tested"])
@limiter.limit("10/minute")
async def search(
    request: Request,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> dict:
    service = SystemAdminService(db)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/disable", response_model=SystemAdminAccountOut, tags=["system-admin: tested"])
@limiter.limit("10/minute")
async def disable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> SystemAdminAccountOut:
    service = SystemAdminService(db)
    return await service.disable_by_id(user, id, True)


@router.patch("/{id}/enable", response_model=SystemAdminAccountOut, tags=["system-admin: tested"])
@limiter.limit("10/minute")
async def enable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> SystemAdminAccountOut:
    service = SystemAdminService(db)
    return await service.enable_by_id(user, id, True)


