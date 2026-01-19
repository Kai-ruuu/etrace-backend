from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Query, Depends, UploadFile, Form, File


from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.services.graduate_record import GraduateRecordService
from app.schemas.graduate_record import GraduateRecordOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles


router = APIRouter(tags=["graduate-record"], prefix="/api/v1/insti/graduate-record")


@router.post("/", response_model=GraduateRecordOut)
@limiter.limit("10/minute")
async def create(
    request: Request,
    graduate_record_file: UploadFile | None=File(None),
    graduation_year: int = Form(..., ge=1000),
    course_id: int = Form(..., ge=1),
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> GraduateRecordOut:
    service = GraduateRecordService(db)
    return await service.create(user, graduate_record_file, graduation_year, course_id, True)


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
    service = GraduateRecordService(db)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/archive", response_model=GraduateRecordOut)
@limiter.limit("10/minute")
async def archive(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> GraduateRecordOut:
    service = GraduateRecordService(db)
    return await service.archive_by_id(user, id, True)


@router.patch("/{id}/restore", response_model=GraduateRecordOut)
@limiter.limit("10/minute")
async def restore(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.DEAN])),
) -> GraduateRecordOut:
    service = GraduateRecordService(db)
    return await service.restore_by_id(user, id, True)


