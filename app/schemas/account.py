from datetime import datetime
from pydantic import BaseModel, EmailStr

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
    dean_profile: DeanProfileOut
    model_config = {"from_attributes": True}


class AlumniAccountOut(AccountOutBase):
    alumni_profile: AlumniProfileOut
    model_config = {"from_attributes": True}


class CompanyAccountOut(AccountOutBase):
    company_profile: CompanyProfileOut
    model_config = {"from_attributes": True}


class PesoStaffAccountOut(AccountOutBase):
    peso_staff_profile: PesoStaffProfileOut
    model_config = {"from_attributes": True}


class SystemAdminAccountOut(AccountOutBase):
    system_admin_profile: SystemAdminProfileOut
    model_config = {"from_attributes": True}


class AdminAccountInBase(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str | None = None
    last_name: str
    

class SystemAdminAccountIn(AdminAccountInBase):
    pass
    

class DeanAccountIn(AdminAccountInBase):
    school_id: int
    

class PesoStaffAccountIn(AdminAccountInBase):
    pass


