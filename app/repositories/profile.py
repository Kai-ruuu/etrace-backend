from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import AccountRole, CompanyApprovalStatus, AlumniApprovalStatus
from app.schemas.dean_profile import (
    DeanProfileIn,
    DeanProfileOut
)
from app.schemas.alumni_profile import AlumniProfileOut
from app.schemas.company_profile import (
    CompanyProfileIn,
    CompanyProfileOut
)
from app.schemas.peso_staff_profile import (
    PesoStaffProfileIn,
    PesoStaffProfileOut
)
from app.schemas.system_admin_profile import (
    SystemAdminProfileIn,
    SystemAdminProfileOut
)
from app.models.account import Account
from app.models.dean_profile import DeanProfile
from app.models.alumni_profile import AlumniProfile
from app.models.company_profile import CompanyProfile
from app.models.peso_staff_profile import PesoStaffProfile
from app.models.system_admin_profile import SystemAdminProfile


class ProfileRepository:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db
        self.role = role


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
        id: int
    ) -> (
        None |
        DeanProfile |
        AlumniProfile |
        CompanyProfile |
        PesoStaffProfile |
        SystemAdminProfile
    ):
        statement = (
            select(self.ProfileModel)
            .join(Account, Account.id == self.ProfileModel.account_id)
            .where(
                self.ProfileModel.id == id,
                Account.role == self.role
            )
        )
        result = await self.db.execute(statement)
        profile = result.scalar_one_or_none()

        if not profile:
            return None
        
        return profile
    
    
    async def get_by_account_id(
        self,
        account_id: int
    ) -> (
        None |
        DeanProfile |
        AlumniProfile |
        CompanyProfile |
        PesoStaffProfile |
        SystemAdminProfile
    ):
        statement = (
            select(self.ProfileModel)
            .join(Account, Account.id == self.ProfileModel.account_id)
            .where(
                self.ProfileModel.account_id == account_id,
                Account.role == self.role
            )
        )
        result = await self.db.execute(statement)
        profile = result.scalar_one_or_none()

        if not profile:
            return None
        
        return profile
    
    
    async def approve_company_as_system_admin_by_account_id(
        self,
        account_id: int
    ) -> CompanyProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.sysad_approval_status = CompanyApprovalStatus.APPROVED
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def reject_company_as_system_admin_by_account_id(self, account_id: int) -> CompanyProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.sysad_approval_status = CompanyApprovalStatus.REJECTED
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def pend_company_as_system_admin_by_account_id(self, account_id: int) -> CompanyProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.sysad_approval_status = CompanyApprovalStatus.PENDING
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def approve_company_as_peso_staff_by_account_id(self, account_id: int) -> CompanyProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.peso_staff_approval_status = CompanyApprovalStatus.APPROVED
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def reject_company_as_peso_staff_by_account_id(self, account_id: int) -> CompanyProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.peso_staff_approval_status = CompanyApprovalStatus.REJECTED
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
        
    
    async def pend_company_as_peso_staff_by_account_id(self, account_id: int) -> CompanyProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.peso_staff_approval_status = CompanyApprovalStatus.PENDING
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def approve_alumni(self, account_id: int) -> AlumniProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.dean_approval_status = AlumniApprovalStatus.APPROVED
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def reject_alumni(self, account_id: int) -> AlumniProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.dean_approval_status = AlumniApprovalStatus.REJECTED
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    
    async def pend_alumni(self, account_id: int) -> AlumniProfile:
        db_profile = await self.get_by_account_id(account_id, False)
        db_profile.dean_approval_status = AlumniApprovalStatus.PENDING
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile


    async def update(
        self,
        profile_id: int,
        profile: SystemAdminProfileIn | DeanProfileIn | PesoStaffProfileIn | CompanyProfileIn,
    ) -> (
        SystemAdminProfile |
        DeanProfile |
        PesoStaffProfile |
        CompanyProfile
    ):
        statement = (
            update(self.ProfileModel)
            .where(self.ProfileModel.id == profile_id)
            .values({
                attribute: value
                for attribute, value in profile.model_dump().items()
                    if value is not None and str(value).strip() != ""
            })
        )

        await self.db.execute(statement)
        await self.db.commit()
        return await self.get_by_id(profile_id)
    
    
    async def update_dean_school_by_id(
        self,
        profile_id: int,
        school_id: int
    ) -> DeanProfile:
        statement = (
            update(DeanProfile)
            .where(DeanProfile.id == profile_id)
            .values({"school_id": school_id})
        )
        await self.db.execute(statement)
        await self.db.commit()
        return await self.get_by_id(profile_id)
    
        
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


