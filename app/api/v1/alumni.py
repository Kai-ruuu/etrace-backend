from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Query, Request, Depends, UploadFile, Form, File

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.core.enums import AlumniApprovalStatus
from app.services.alumni import AlumniService
from app.services.profile import ProfileService
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.schemas.account import AlumniAccountOut
from app.schemas.alumni_profile import (
    AlumniProfileOut,
    AlumniOccupationLocationIn,
)


router = APIRouter(tags=["alumni"], prefix="/api/v1/alumni")


@router.patch("/")
@limiter.limit("30/minute")
async def update(
    request: Request,
    address: str | None = Form(None),
    phone_number: str | None = Form(None),
    profile_picture_file: UploadFile | None = File(None),
    curriculum_vitae_file: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> AlumniProfileOut:
    service = ProfileService(db, user.role)
    return await service.update_as_alumni(
        user,
        address,
        phone_number,
        profile_picture_file,
        curriculum_vitae_file,
        True
    )


@router.get("/search")
@limiter.limit("30/minute")
async def search(
    request: Request,
    approval_status: AlumniApprovalStatus | None = None,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> dict:
    service = AlumniService(db)
    return await service.search(user, approval_status, query, page, page_size)


@router.get("/{id}")
# @limiter.limit("30/minute")
async def search(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> dict:
    service = AlumniService(db)
    return await service.get_by_id(user, id, True)


@router.post("/geocode-occupation-location")
@limiter.limit("30/minute")
async def geocode_occupation_location(
    request: Request,
    location: AlumniOccupationLocationIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI, AccountRole.DEAN, AccountRole.COMPANY])),
) -> dict:
    service = AlumniService(db)
    return await service.geocode_occupation_location(user, location)


@router.patch("/{id}/disable", response_model=AlumniAccountOut)
@limiter.limit("30/minute")
async def disable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.disable_by_id(user, id, True)


@router.patch("/{id}/enable", response_model=AlumniAccountOut)
@limiter.limit("30/minute")
async def enable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.enable_by_id(user, id, True)


@router.patch("/{id}/approve", response_model=AlumniAccountOut)
@limiter.limit("30/minute")
async def approve(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.approve_by_id(user, id, True)


@router.patch("/{id}/reject", response_model=AlumniAccountOut)
@limiter.limit("30/minute")
async def reject(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.reject_by_id(user, id, True)


@router.patch("/{id}/pend", response_model=AlumniAccountOut)
@limiter.limit("30/minute")
async def pend(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> AlumniAccountOut:
    service = AlumniService(db)
    return await service.pend_by_id(user, id, True)