from datetime import datetime
from pydantic import BaseModel

from app.core.enums import AlumniApprovalStatus, AlumniEmploymentStatus

class AlumniProfileBase(BaseModel):
    profile_picture_filename: str
    curriculum_vitae_filename: str
    first_name: str
    middle_name: str
    last_name: str
    account_id: int
    prefix: str | None = None
    first_name: str
    middle_name: str | None = None
    last_name: str
    model_config = {"from_attributes": True}

class AlumniProfileOut(AlumniProfileBase):
    id: int
    account_id: int
    dean_approval_status: AlumniApprovalStatus
    employment_status: AlumniEmploymentStatus
    year_graduated: int
    # occupation_states: list
    address: str
    phone_number: str
    # socials: list
    course_id: int
    # course: CourseOut
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}