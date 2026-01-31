from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Query, Depends, APIRouter

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.schemas.job_post import JobPostIn, JobPostOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.services.job_post import JobPostService
from app.services.job_post_interest import JobPostInterestService


router = APIRouter(tags=["job-post"], prefix="/api/v1/job-post")


@router.post("/", response_model=JobPostOut)
@limiter.limit("10/minute")
async def create(
    request: Request,
    job_post: JobPostIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.create(user, job_post, True)


@router.get("/search")
@limiter.limit("10/minute")
async def search(
    request: Request,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY, AccountRole.ALUMNI])),
) -> dict:
    service = JobPostService(db)
    return await service.search(user, query, page, page_size)


@router.get("/list-for-alumni")
@limiter.limit("10/minute")
async def get_alumni_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> dict:
    service = JobPostService(db)
    return await service.get_alumni_list(user, page, page_size)


@router.get("/list-for-company")
@limiter.limit("10/minute")
async def get_company_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> dict:
    service = JobPostService(db)
    return await service.get_company_list(user, page, page_size)


@router.patch("/{id}/archive", response_model=JobPostOut)
@limiter.limit("10/minute")
async def archive(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.archive_by_id(user, id, True)


@router.patch("/{id}/restore", response_model=JobPostOut)
@limiter.limit("10/minute")
async def restore(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.restore_by_id(user, id, True)


@router.patch("/{id}/unpublish", response_model=JobPostOut)
@limiter.limit("10/minute")
async def unpublish(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.unpublish_by_id(user, id, True)


@router.patch("/{id}/publish", response_model=JobPostOut)
@limiter.limit("10/minute")
async def publish(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.publish_by_id(user, id, True)


@router.delete("/{id}/dislike", response_model=JobPostOut)
@limiter.limit("10/minute")
async def dislike(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.dislike_by_id(user, id, True)


@router.post("/{id}/like", response_model=JobPostOut)
@limiter.limit("10/minute")
async def like(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.like_by_id(user, id, True)


@router.post("/{id}/send-cv", response_model=JobPostOut)
@limiter.limit("10/minute")
async def send_cv(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.send_cv_by_id(user, id, True)


@router.get("/{id}/get-interested")
@limiter.limit("10/minute")
async def get_interested(
    request: Request,
    id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> dict:
    service = JobPostInterestService(db)
    return await service.get_company_list(user, id, page, page_size)


@router.get("/{id}/get-interests")
@limiter.limit("10/minute")
async def get_interests(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> dict:
    service = JobPostInterestService(db)
    return await service.get_alumni_list(user, page, page_size)