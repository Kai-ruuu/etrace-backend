from fastapi import Request, Query, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.schemas.account import AlumniAccountOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.services.alumni import AlumniService


router = APIRouter(tags=["alumni"], prefix="/api/v1/user/alumni")


@router.get("/search")
@limiter.limit("10/minute")
async def search(
    request: Request,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> dict:
    service = AlumniService(db)
    return await service.search(user, query, page, page_size)


@router.get("/{id}/location-info")
@limiter.limit("10/minute")
async def get_location_info(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI, AccountRole.DEAN, AccountRole.COMPANY])),
) -> dict:
    service = AlumniService(db)
    return await service.get_location_info(user, id)


@router.patch("/{id}/disable", response_model=AlumniAccountOut)
@limiter.limit("10/minute")
async def disable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.disable_by_id(user, id, True)


@router.patch("/{id}/enable", response_model=AlumniAccountOut)
@limiter.limit("10/minute")
async def enable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.enable_by_id(user, id, True)


@router.patch("/{id}/approve", response_model=AlumniAccountOut)
@limiter.limit("10/minute")
async def approve(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.approve_by_id(user, id, True)


@router.patch("/{id}/reject", response_model=AlumniAccountOut)
@limiter.limit("10/minute")
async def reject(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.reject_by_id(user, id, True)


@router.patch("/{id}/pend", response_model=AlumniAccountOut)
@limiter.limit("10/minute")
async def pend(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.pend_by_id(user, id, True)
