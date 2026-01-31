from fastapi import Request, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.core.enums import AccountRole
from app.utils.rate_limiting import limiter
from app.services.profile import ProfileService
from app.core.dependencies import get_db, allow_roles
from app.schemas.dean_profile import DeanProfileOut, DeanProfileIn
from app.schemas.peso_staff_profile import PesoStaffProfileOut, PesoStaffProfileIn
from app.schemas.system_admin_profile import SystemAdminProfileOut, SystemAdminProfileIn


router = APIRouter(tags=["account"], prefix="/api/v1/user/profile")


@router.patch("/update-as-admin")
@limiter.limit("10/minute")
async def change_password(
    request: Request,
    profile_id: int,
    profile: SystemAdminProfileIn | DeanProfileIn | PesoStaffProfileIn,
    db: AsyncSession = Depends(get_db),
    user: Account = Depends(allow_roles([AccountRole.SYSTEM_ADMIN, AccountRole.DEAN, AccountRole.PESO_STAFF])),
) -> (
    SystemAdminProfileOut |
    DeanProfileOut |
    PesoStaffProfileOut
):
    service = ProfileService(db, user.role)
    return await service.update_as_admin_by_id(user, profile_id, profile, True)
