from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, literal

from app.core.enums import AccountRole
from app.core.enums import (
    AlumniApprovalStatus,
    CompanyApprovalStatus
)
from app.utils.password import hash_password
from app.models.account import Account
from app.models.occupation import Occupation
from app.models.occupation_state import OccupationState
from app.models.dean_profile import DeanProfile
from app.models.alumni_profile import AlumniProfile
from app.models.company_profile import CompanyProfile
from app.models.peso_staff_profile import PesoStaffProfile
from app.models.system_admin_profile import SystemAdminProfile


class AccountRepository:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db
        self.role = role

    
    def get_filter_statement(self, query: str | None):
        match self.role:
            case AccountRole.SYSTEM_ADMIN:
                return or_(
                    Account.email.ilike(f"%{query}%"),
                    self.AccountProfileModel.first_name.ilike(f"%{query}%"),
                    func.coalesce(self.AccountProfileModel.middle_name, literal("")).ilike(f"%{query}%"),
                    self.AccountProfileModel.last_name.ilike(f"%{query}%"),
                )
            case AccountRole.PESO_STAFF:
                return or_(
                    Account.email.ilike(f"%{query}%"),
                    self.AccountProfileModel.first_name.ilike(f"%{query}%"),
                    func.coalesce(self.AccountProfileModel.middle_name, literal("")).ilike(f"%{query}%"),
                    self.AccountProfileModel.last_name.ilike(f"%{query}%"),
                )
            case AccountRole.COMPANY:
                return or_(
                    Account.email.ilike(f"%{query}%"),
                    self.AccountProfileModel.name.ilike(f"%{query}%"),
                    self.AccountProfileModel.address.ilike(f"%{query}%"),
                )
            case AccountRole.ALUMNI:
                return or_(
                    Account.email.ilike(f"%{query}%"),
                    func.coalesce(self.AccountProfileModel.name_extension, literal("")).ilike(f"%{query}%"),
                    self.AccountProfileModel.first_name.ilike(f"%{query}%"),
                    func.coalesce(self.AccountProfileModel.middle_name, literal("")).ilike(f"%{query}%"),
                    self.AccountProfileModel.last_name.ilike(f"%{query}%"),
                )
            case AccountRole.DEAN:
                return or_(
                    Account.email.ilike(f"%{query}%"),
                    self.AccountProfileModel.first_name.ilike(f"%{query}%"),
                    func.coalesce(self.AccountProfileModel.middle_name, literal("")).ilike(f"%{query}%"),
                    self.AccountProfileModel.last_name.ilike(f"%{query}%"),
                )
            case _:
                raise ValueError("Invalid role value.")
    
    
    async def create(self, account: Account) -> Account:
        self.db.add(account)
        await self.db.flush()
        await self.db.refresh(account)
        return account
        
    
    async def get_by_id(self, id: int) -> Account | None:
        statement = (
            select(Account)
            .options(self.AccountProfileLoad)
            .where(
                Account.id == id,
                Account.role == self.role
            )
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
        

    async def get_alumni_by_id(self, id: int) -> Account | None:
        statement = (
            select(Account)
            .options(
                selectinload(Account.alumni_profile)
                    .selectinload(AlumniProfile.course),

                selectinload(Account.alumni_profile)
                    .selectinload(AlumniProfile.occupation_states)
                    .selectinload(OccupationState.occupation),
                    
                selectinload(Account.alumni_profile)
                    .selectinload(AlumniProfile.socials)
            )
            .where(
                Account.id == id,
                Account.role == AccountRole.ALUMNI
            )
        )

        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
        
        
    async def get_by_email(self, email: str) -> Account | None:
        statement = (
            select(Account)
            .options(self.AccountProfileLoad)
            .where(
                Account.email == email,
                Account.role == self.role
            )
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    
    
    async def disable(self, db_account: Account) -> Account:
        db_account.is_disabled = True

        await self.db.commit()
        await self.db.refresh(db_account, attribute_names=self.AccountProfileAttrName)
        return db_account
    
    
    async def enable(self, db_account: Account) -> Account:
        db_account.is_disabled = False

        await self.db.commit()
        await self.db.refresh(db_account, attribute_names=self.AccountProfileAttrName)
        return db_account
    

    async def search(
        self,
        query: str | None = None,
        page: int = 1,
        page_size: int = 20,
        *,
        dean_approval_status: AlumniApprovalStatus | None = None,
        sysad_approval_status: CompanyApprovalStatus | None = None,
        peso_staff_approval_status: CompanyApprovalStatus | None = None,
    ) -> tuple[list[Account], int, int]:
        filters = [Account.role == self.role]
    
        if query:
            filters.append(self.get_filter_statement(query))
    
        if dean_approval_status is not None:
            filters.append(self.AccountProfileModel.dean_approval_status == dean_approval_status)
        elif sysad_approval_status is not None:
            filters.append(self.AccountProfileModel.sysad_approval_status == sysad_approval_status)
        elif peso_staff_approval_status is not None:
            filters.append(self.AccountProfileModel.peso_staff_approval_status == peso_staff_approval_status)

        search_statement = (
            select(Account)
            .options(self.AccountProfileLoad)
            .join(self.AccountProfileModel)
            .where(*filters)
        )
        
        count_statement = (
            select(func.count())
            .select_from(Account)
            .join(self.AccountProfileModel)
            .where(*filters)
        )

        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size

        search_statement = search_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        accounts = result.scalars().unique().all()

        return accounts, total, total_pages
    
    
    async def change_password(self, account: Account, new_password: str) -> Account:
        account.password = hash_password(new_password)
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    
    @property
    def AccountProfileModel(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return SystemAdminProfile
            case AccountRole.PESO_STAFF: return PesoStaffProfile
            case AccountRole.COMPANY: return CompanyProfile
            case AccountRole.ALUMNI: return AlumniProfile
            case AccountRole.DEAN: return DeanProfile
            case _: raise ValueError("Invalid role value.")

        
    @property
    def AccountProfileAttrName(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return ["system_admin_profile"]
            case AccountRole.PESO_STAFF: return ["peso_staff_profile"]
            case AccountRole.COMPANY: return ["company_profile"]
            case AccountRole.ALUMNI: return ["alumni_profile"]
            case AccountRole.DEAN: return ["dean_profile"]


    @property
    def AccountProfileLoad(self):
        match self.role:
            case AccountRole.SYSTEM_ADMIN: return selectinload(Account.system_admin_profile)
            case AccountRole.PESO_STAFF: return selectinload(Account.peso_staff_profile)
            case AccountRole.COMPANY: return selectinload(Account.company_profile)
            case AccountRole.ALUMNI: return selectinload(Account.alumni_profile).selectinload(AlumniProfile.course)
            case AccountRole.DEAN: return selectinload(Account.dean_profile).selectinload(DeanProfile.school)