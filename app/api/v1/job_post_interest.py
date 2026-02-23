from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Query, Depends, APIRouter

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.services.job_post_interest import JobPostInterestService
from app.schemas.job_post_interest import JobPostInterestCompanyListOut


router = APIRouter(tags=["job-post-interest"], prefix="/api/v1/job-post-interest")


@router.patch("/{id}/unreview", response_model=JobPostInterestCompanyListOut)
@limiter.limit("30/minute")
async def unreview(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostInterestCompanyListOut:
    service = JobPostInterestService(db)
    return await service.mark_as_not_reviewed(user, id, True)


@router.patch("/{id}/review", response_model=JobPostInterestCompanyListOut)
@limiter.limit("30/minute")
async def review(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostInterestCompanyListOut:
    service = JobPostInterestService(db)
    return await service.mark_as_reviewed(user, id, True)
