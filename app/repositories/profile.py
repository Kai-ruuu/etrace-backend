from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, literal

from app.core.enums import AccountRole
from app.schemas.dean_profile import DeanProfileOut
from app.schemas.alumni_profile import AlumniProfileOut
from app.schemas.company_profile import CompanyProfileOut
from app.schemas.peso_staff_profile import PesoStaffProfileOut
from app.schemas.system_admin_profile import SystemAdminProfileOut
from app.models.account import Account
from app.models.dean_profile import DeanProfile
from app.models.alumni_profile import AlumniProfile
from app.models.company_profile import CompanyProfile
from app.models.peso_staff_profile import PesoStaffProfile
from app.models.system_admin_profile import SystemAdminProfile

class ProfileRepository:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db

    async def create(
        self,
        profile: (
            SystemAdminProfile |
            PesoStaffProfile |
            CompanyProfile |
            AlumniProfile |
            DeanProfile
        )
    ) -> (
        SystemAdminProfile |
        PesoStaffProfile |
        CompanyProfile |
        AlumniProfile |
        DeanProfile
    ):
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile
    
    async def get_by_id(
        self,
        id: int,
        as_pymodel: bool = False
    ) -> (
        None |
        DeanProfile |
        AlumniProfile |
        CompanyProfile |
        PesoStaffProfile |
        SystemAdminProfile |
        DeanProfileOut |
        AlumniProfileOut |
        CompanyProfileOut |
        PesoStaffProfileOut |
        SystemAdminProfileOut
    ):
        statement = (
            select(self.ProfileModel)
            .join(Account, Account.id == self.ProfileModel.account_id)
            .where(
                self.ProfileModel.id == id,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        profile = result.scalar_one_or_none()

        if not profile:
            return None
        
        return SystemAdminProfileOut.model_validate(profile) if as_pymodel else profile
    
    async def get_by_account_id(
        self,
        account_id: int,
        as_pymodel: bool = False
    ) -> (
        None |
        DeanProfile |
        AlumniProfile |
        CompanyProfile |
        PesoStaffProfile |
        SystemAdminProfile |
        DeanProfileOut |
        AlumniProfileOut |
        CompanyProfileOut |
        PesoStaffProfileOut |
        SystemAdminProfileOut
    ):
        statement = (
            select(SystemAdminProfile)
            .join(Account, Account.id == SystemAdminProfile.account_id)
            .where(
                SystemAdminProfile.account_id == account_id,
                Account.role == AccountRole.SYSTEM_ADMIN
            )
        )
        result = await self.db.execute(statement)
        profile = result.scalar_one_or_none()

        if not profile:
            return None
        
        return self.ProfilePymodel.model_validate(profile) if as_pymodel else profile
    
    
    @property
    def ProfileModel(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return SystemAdminProfile
            case AccountRole.PESO_STAFF: return PesoStaffProfile
            case AccountRole.COMPANY: return CompanyProfile
            case AccountRole.ALUMNI: return AlumniProfile
            case AccountRole.DEAN: return DeanProfile
            case _: raise ValueError("Invalid role value.")
    
    
    @property
    def ProfilePymodel(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return SystemAdminProfileOut
            case AccountRole.PESO_STAFF: return PesoStaffProfileOut
            case AccountRole.COMPANY: return CompanyProfileOut
            case AccountRole.ALUMNI: return AlumniProfileOut
            case AccountRole.DEAN: return DeanProfileOut
            case _: raise ValueError("Invalid role value.")


