from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Query, Depends, APIRouter


from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.schemas.occupation import OccupationOut
from app.services.occupation import OccupationService
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles


router = APIRouter(tags=["occupation"], prefix="/api/v1/insti/occupation")


@router.get("")
# @limiter.limit("30/minute")
async def get_all(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> list[OccupationOut]:
    service = OccupationService(db)
    return await service.get_all(True)


@router.get("/search-with-course-id")
@limiter.limit("30/minute")
async def search_with_course_id(
    request: Request,
    course_id: int,
    aligned: bool | None = None,
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> dict:
    service = OccupationService(db)
    return await service.search_with_course_id(user, course_id, aligned, query, page, page_size)


@router.delete("/{course_id}/{occupation_id}/unalign", response_model=OccupationOut)
@limiter.limit("30/minute")
async def unalign(
    request: Request,
    course_id: int,
    occupation_id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> OccupationOut:
    service = OccupationService(db)
    return await service.unalign_by_course_and_occupation_id(user, course_id, occupation_id, True)


@router.post("/{course_id}/{occupation_id}/align", response_model=OccupationOut)
@limiter.limit("30/minute")
async def align(
    request: Request,
    course_id: int,
    occupation_id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> OccupationOut:
    service = OccupationService(db)
    return await service.align_by_course_and_occupation_id(user, course_id, occupation_id, True)


