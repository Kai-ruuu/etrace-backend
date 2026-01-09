from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.enums.all import AccountRole
from app.schemas.dean import DeanAdminProfileOut
from app.schemas.alumni import AlumniProfileOut
from app.schemas.company import CompanyProfileOut
from app.schemas.peso_staff import PesoStaffProfileOut
from app.schemas.system_admin import SystemAdminProfileOut

class AccountBase(BaseModel):
    id: int
    role: AccountRole
    email: EmailStr
    is_disabled: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class SystemAdminAccountOut(AccountBase):
    profile: SystemAdminProfileOut
    model_config = {"from_attributes": True}

class DeanAccountOut(AccountBase):
    profile: DeanAdminProfileOut
    model_config = {"from_attributes": True}

class PesoStaffAccountOut(AccountBase):
    profile: PesoStaffProfileOut
    model_config = {"from_attributes": True}

class CompanyAccountOut(AccountBase):
    profile: CompanyProfileOut
    model_config = {"from_attributes": True}

class AlumniAccountOut(AccountBase):
    profile: AlumniProfileOut
    model_config = {"from_attributes": True}

class AdminAccountBaseIn(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str | None
    last_name: str

class SystemAdminAccountIn(AdminAccountBaseIn):
    pass

class DeanAccountIn(AdminAccountBaseIn):
    school_id: int

class PesoStaffAccountIn(AdminAccountBaseIn):
    pass

