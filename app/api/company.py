from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Query, Depends, APIRouter

from app.models.account import Account
from app.schemas.account import CompanyAccountOut
from app.core.enums import AccountRole
from app.core.dependencies import get_db, allow_roles
from app.services.company import CompanyService


router = APIRouter(tags=["company"], prefix="/api/v1/user/company")
   

@router.get("/search", tags=["company: tested"])
async def search(
    query: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=20, le=100),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> dict:
    service = CompanyService(db)
    return await service.search(user, query, page, page_size)


@router.patch("/{id}/disable", response_model=CompanyAccountOut, tags=["company: tested"])
async def disable(
    id: int,
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.disable_by_id(user, id, True)


@router.patch("/{id}/enable", response_model=CompanyAccountOut, tags=["company: tested"])
async def enable(
    id: int,
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN])),
    db: AsyncSession = Depends(get_db)
) -> CompanyAccountOut:
    service = CompanyService(db)
    return await service.enable_by_id(user, id, True)


