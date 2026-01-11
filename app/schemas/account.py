from datetime import datetime
from pydantic import BaseModel

from app.core.enums import AccountRole
from app.schemas.dean_profile import DeanProfileOut
from app.schemas.alumni_profile import AlumniProfileOut
from app.schemas.company_profile import CompanyProfileOut
from app.schemas.peso_staff_profile import PesoStaffProfileOut
from app.schemas.system_admin_profile import SystemAdminProfileOut

class AccountBase(BaseModel):
    email: str
    model_config = {"from_attributes": True}
    
class AccountOutBase(AccountBase):
    id: int
    role: AccountRole
    is_disabled: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class DeanAccountOut(AccountOutBase):
    profile: DeanProfileOut
    model_config = {"from_attributes": True}

class AlumniAccountOut(AccountOutBase):
    profile: AlumniProfileOut
    model_config = {"from_attributes": True}

class CompanyAccountOut(AccountOutBase):
    profile: CompanyProfileOut
    model_config = {"from_attributes": True}

class PesoStaffAccountOut(AccountOutBase):
    profile: PesoStaffProfileOut
    model_config = {"from_attributes": True}

class SystemAdminAccountOut(AccountOutBase):
    profile: SystemAdminProfileOut
    model_config = {"from_attributes": True}
    
    @classmethod
    def from_account(cls, account):
        return cls(
            id=account.id,
            email=account.email,
            role=account.role,
            is_disabled=account.is_disabled,
            created_at=account.created_at,
            updated_at=account.updated_at,
            profile=account.system_admin_profile
        )