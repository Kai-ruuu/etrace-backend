from datetime import datetime
from pydantic import BaseModel

from app.enums.all import CompanyApprovalStatus

class CompanyProfileBase(BaseModel):
    id: int
    name: str
    logo_filename: str
    sec_filename: str
    profile_filename: str
    business_permit_filename: str
    list_of_vacancies_filename: str
    cert_from_dole_filename: str
    cert_of_no_pending_case_filename: str
    reg_dti_cda_filename: str
    reg_of_est_filename: str
    reg_philjobnet_filename: str
    account_id: int
    sysad_approval_status: CompanyApprovalStatus
    peso_staff_approval_status: CompanyApprovalStatus
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class CompanyProfileOut(CompanyProfileBase):
    model_config = {"from_attributes": True}

