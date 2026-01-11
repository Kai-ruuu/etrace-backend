from fastapi import Query, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.account import Account
from app.services.school import SchoolService
from app.schemas.school import SchoolIn, SchoolOut
from app.repositories.school import SchoolRepository
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles


router = APIRouter(tags=["system-admin", "school"], prefix="/api/v1/insti/school")


@router.post("/", response_model=SchoolOut, tags=["tested"])
async def create(
    school: SchoolIn,
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> SchoolOut:
    repo = SchoolRepository(db)
    service = SchoolService(db, repo)
    return await service.create(user, school, True)
    

@router.get("/search", tags=["tested"])
async def search(
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> dict:
    repo = SchoolRepository(db)
    service = SchoolService(db, repo)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/archive", response_model=SchoolOut, tags=["tested"])
async def archive(
    id: int,
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> SchoolOut:
    repo = SchoolRepository(db)
    service = SchoolService(db, repo)
    return await service.archive_by_id(user, id, True)


@router.patch("/{id}/restore", response_model=SchoolOut, tags=["tested"])
async def restore(
    id: int,
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> SchoolOut:
    repo = SchoolRepository(db)
    service = SchoolService(db, repo)
    return await service.restore_by_id(user, id, True)


