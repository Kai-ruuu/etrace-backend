from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.password import verify_password
from app.core.exceptions import *
from app.core.enums import AccountRole, Action
from app.repositories.school import SchoolRepository
from app.repositories.profile import ProfileRepository
from app.models.account import Account
from app.models.dean_profile import DeanProfile
from app.models.peso_staff_profile import PesoStaffProfile
from app.models.system_admin_profile import SystemAdminProfile
from app.schemas.dean_profile import DeanProfileOut, DeanProfileIn
from app.schemas.peso_staff_profile import PesoStaffProfileOut, PesoStaffProfileIn
from app.schemas.system_admin_profile import SystemAdminProfileOut, SystemAdminProfileIn


class ProfileService:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db
        self.role = role
        self.school_repo = SchoolRepository(self.db)
        self.profile_repo = ProfileRepository(self.db, role)
        
    
    async def update_as_admin_by_id(
        self,
        user: Account,
        profile_id: int,
        profile: SystemAdminProfileIn | DeanProfileIn | PesoStaffProfileIn,
        as_py_model: bool = False
    ) -> (
        SystemAdminProfile |
        DeanProfile |
        PesoStaffProfile |
        SystemAdminProfileOut |
        DeanProfileOut |
        PesoStaffProfileOut
    ):
        if user.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
    
        db_profile = await self.profile_repo.get_by_id(profile_id)
        
        if not db_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
        
        updated_db_profile = await self.profile_repo.update_as_admin_by_id(profile_id, profile)
        return self.ProfilePymodel.model_validate(updated_db_profile) if as_py_model else updated_db_profile
    
    async def update_dean_school_by_id(
        self,
        user: Account,
        profile_id: int,
        school_id: int,
        as_pymodel: bool = False
    ) -> DeanProfile | DeanProfileOut:
        user.permissions.raise_unauthorized_if_excludes(Action.UPDATE_DEAN_SCHOOL)

        db_school = await self.school_repo.get_by_id(school_id)

        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION

        db_dean_profile = await self.profile_repo.get_by_id(profile_id)

        if not db_dean_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
        
        updated_db_profile = await self.profile_repo.update_dean_school_by_id(profile_id, school_id)
        return DeanProfileOut.model_validate(updated_db_profile) if as_pymodel else updated_db_profile
        
    
    @property
    def ProfilePymodel(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return SystemAdminProfileOut
            case AccountRole.DEAN: return DeanProfileOut
            case AccountRole.PESO_STAFF: return PesoStaffProfileOut
            case _: raise ValueError("Invalid role value.")
