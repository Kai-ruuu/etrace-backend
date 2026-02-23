from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Query, Depends, APIRouter


from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.services.course import CourseService
from app.schemas.course import CourseIn, CourseOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles, get_current_user


router = APIRouter(tags=["course"], prefix="/api/v1/insti/course")


@router.get("", response_model=list[CourseOut])
@limiter.limit("30/minute")
async def get_all(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> list[CourseOut]:
    service = CourseService(db)
    return await service.get_all(True)


@router.post("", response_model=CourseOut)
@limiter.limit("30/minute")
async def create(
    request: Request,
    course: CourseIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.DEAN])),
) -> CourseOut:
    service = CourseService(db)
    return await service.create(user, course, True)
    

@router.get("/search")
@limiter.limit("30/minute")
async def search(
    request: Request,
    query: str | None = None,
    archived: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.DEAN])),
) -> dict:
    service = CourseService(db)
    return await service.search(user, query, archived, page, page_size)
    

@router.get("/dean-list", response_model=list[CourseOut])
@limiter.limit("30/minute")
async def search(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> list[CourseOut]:
    service = CourseService(db)
    return await service.get_dean_list(user, True)


@router.patch("/{id}/archive", response_model=CourseOut)
@limiter.limit("30/minute")
async def archive(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> CourseOut:
    service = CourseService(db)
    return await service.archive_by_id(user, id, True)


@router.patch("/{id}/restore", response_model=CourseOut)
@limiter.limit("30/minute")
async def restore(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> CourseOut:
    service = CourseService(db)
    return await service.restore_by_id(user, id, True)


