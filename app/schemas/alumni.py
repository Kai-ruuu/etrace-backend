from datetime import datetime
from pydantic import BaseModel

from app.enums.all import AlumniApprovalStatus, AlumniEmploymentStatus
from app.schemas.course import CourseBase

class AlumniProfileBase(BaseModel):
    id: int
    profile_picture_filename: int
    curriculum_vitae_filename: str | None = None
    dean_approval_status: AlumniApprovalStatus
    employment_status: AlumniEmploymentStatus
    prefix: str | None = None
    first_name: str
    middle_name: str | None = None
    last_name: str
    year_graduated: int
    address: str
    phone_number: str
    course_id: int
    account_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class AlumniProfileOut(AlumniProfileBase):
    course: CourseBase
    model_config = {"from_attributes": True}

