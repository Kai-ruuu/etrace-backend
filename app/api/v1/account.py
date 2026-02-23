from fastapi import Request, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.services.account import AccountService
from app.core.dependencies import get_db, get_current_user
from app.schemas.account import ChangePasswordIn
from app.schemas.account import (
    SystemAdminAccountOut,
    DeanAccountOut,
    PesoStaffAccountOut,
    CompanyAccountOut,
    AlumniAccountOut
)


router = APIRouter(tags=["account"], prefix="/api/v1/account")


@router.patch("/change-password")
@limiter.limit("30/minute")
async def change_password(
    request: Request,
    change_password_info: ChangePasswordIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(get_current_user),
) -> (
    SystemAdminAccountOut |
    DeanAccountOut |
    PesoStaffAccountOut |
    CompanyAccountOut |
    AlumniAccountOut
):
    service = AccountService(db, user.role)
    return await service.change_password(user, change_password_info, True)
