from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Query, Request, Depends, UploadFile, Form, File

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.services.profile import ProfileService
from app.services.company import CompanyService
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.schemas.account import CompanyAccountOut
from app.schemas.company_profile import CompanyProfileOut


router = APIRouter(tags=["company"], prefix="/api/v1/company")


@router.patch("/")
@limiter.limit("30/minute")
async def update(
    request: Request,
    name: str | None=Form(None),
    address: str | None=Form(None),
    logo_file: UploadFile | None=File(None),
    sec_file: UploadFile | None=File(None),
    profile_file: UploadFile | None=File(None),
    business_permit_file: UploadFile | None=File(None),
    list_of_vacancies_file: UploadFile | None=File(None),
    cert_from_dole_file: UploadFile | None=File(None),
    cert_of_no_pending_case_file: UploadFile | None=File(None),
    reg_dti_cda_file: UploadFile | None=File(None),
    reg_of_est_file: UploadFile | None=File(None),
    reg_philjobnet_file: UploadFile | None=File(None),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> CompanyProfileOut:
    service = ProfileService(db, user.role)
    return await service.update_as_company(
        user,
        name,
        address,
        logo_file,
        sec_file,
        profile_file,
        business_permit_file,
        list_of_vacancies_file,
        cert_from_dole_file,
        cert_of_no_pending_case_file,
        reg_dti_cda_file,
        reg_of_est_file,
        reg_philjobnet_file,
        True
    )
   

@router.get("/search")
@limiter.limit("30/minute")
async def search(
    request: Request,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.PESO_STAFF])),
) -> dict:
    service = CompanyService(db)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/disable", response_model=CompanyAccountOut)
@limiter.limit("30/minute")
async def disable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.disable_by_id(user, id, True)


@router.patch("/{id}/enable", response_model=CompanyAccountOut)
@limiter.limit("30/minute")
async def enable(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.enable_by_id(user, id, True)


@router.patch("/{id}/approve", response_model=CompanyAccountOut)
@limiter.limit("30/minute")
async def approve(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.PESO_STAFF])),
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.approve_by_id(user, id, True)


@router.patch("/{id}/reject", response_model=CompanyAccountOut)
@limiter.limit("30/minute")
async def reject(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.PESO_STAFF])),
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.reject_by_id(user, id, True)


@router.patch("/{id}/pend", response_model=CompanyAccountOut)
@limiter.limit("30/minute")
async def pend(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.PESO_STAFF])),
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.pend_by_id(user, id, True)


