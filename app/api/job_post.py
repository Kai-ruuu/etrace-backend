from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Query, Depends, APIRouter

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.services.job_post import JobPostService
from app.core.enums import AccountRole
from app.schemas.job_post import JobPostIn, JobPostOut
from app.core.dependencies import get_db, allow_roles


router = APIRouter(tags=["job-post"], prefix="/api/v1/user/job_post")


@router.get("/")
@limiter.limit("10/minute")
async def get_latest(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.ALUMNI])),
) -> dict:
    service = JobPostService(db)
    return await service.get_by_latest(user, page, page_size)


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
async def archive(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.unpublish_by_id(user, id, True)


@router.patch("/{id}/publish", response_model=JobPostOut)
@limiter.limit("10/minute")
async def restore(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.COMPANY])),
) -> JobPostOut:
    service = JobPostService(db)
    return await service.publish_by_id(user, id, True)