from fastapi import Query, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.account import Account
from app.services.course import CourseService
from app.schemas.course import CourseIn, CourseOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles


router = APIRouter(tags=["course"], prefix="/api/v1/insti/course")


@router.post("/", response_model=CourseOut, tags=["course: tested"])
async def create(
    course: CourseIn,
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.DEAN])),
    db: AsyncSession = Depends(get_db)
) -> CourseOut:
    service = CourseService(db)
    return await service.create(user, course, True)
    

@router.get("/search", tags=["course: tested"])
async def search(
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.DEAN])),
    db: AsyncSession = Depends(get_db)
) -> dict:
    service = CourseService(db)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/archive", response_model=CourseOut, tags=["course: tested"])
async def archive(
    id: int,
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
    db: AsyncSession = Depends(get_db)
) -> CourseOut:
    service = CourseService(db)
    return await service.archive_by_id(user, id, True)


@router.patch("/{id}/restore", response_model=CourseOut, tags=["course: tested"])
async def restore(
    id: int,
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
    db: AsyncSession = Depends(get_db)
) -> CourseOut:
    service = CourseService(db)
    return await service.restore_by_id(user, id, True)


