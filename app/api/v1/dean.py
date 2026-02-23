from fastapi import Request, Query, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.schemas.dean_profile import DeanProfileOut, DeanProfileIn
from app.schemas.account import DeanAccountIn, DeanAccountOut
from app.services.dean import DeanService
from app.services.profile import ProfileService
from app.services.account_provision import AccountProvisionService


router = APIRouter(tags=["dean"], prefix="/api/v1/dean")


@router.post("", response_model=DeanAccountOut)
@limiter.limit("30/minute")
async def create(
    request: Request,
    dean: DeanAccountIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> DeanAccountOut:
    service = AccountProvisionService(db, AccountRole.DEAN)
    return await service.create_dean(user, dean, True)


@router.patch("/")
@limiter.limit("30/minute")
async def update(
    request: Request,
    profile: DeanProfileIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> DeanProfileOut:
    service = ProfileService(db, user.role)
    return await service.update(user, profile, True)
    

@router.get("/search")
@limiter.limit("30/minute")
async def search(
    request: Request,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> dict:
    service = DeanService(db)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/disable", response_model=DeanAccountOut)
@limiter.limit("30/minute")
async def disable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> DeanAccountOut:
    service = DeanService(db)
    return await service.disable_by_id(user, id, True)


@router.patch("/{id}/enable", response_model=DeanAccountOut)
@limiter.limit("30/minute")
async def enable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> DeanAccountOut:
    service = DeanService(db)
    return await service.enable_by_id(user, id, True)


@router.patch("/{id}/update-school/{school_id}", response_model=DeanProfileOut)
@limiter.limit("30/minute")
async def update_school(
    request: Request,
    id: int,
    school_id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> DeanProfileOut:
    service = ProfileService(db, AccountRole.DEAN)
    return await service.update_dean_school_by_id(user, id, school_id, True)