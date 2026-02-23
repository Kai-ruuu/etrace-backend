from datetime import datetime
from pydantic import BaseModel

from app.schemas.course import CourseOut
from app.core.enums import AlumniApprovalStatus, AlumniEmploymentStatus


class AlumniProfileBase(BaseModel):
    profile_picture_filename: str
    curriculum_vitae_filename: str
    first_name: str
    middle_name: str
    last_name: str
    account_id: int
    name_extension: str | None = None
    first_name: str
    middle_name: str | None = None
    last_name: str
    model_config = {"from_attributes": True}


class AlumniProfileIn(BaseModel):
    address: str | None
    phone_number: str | None
    profile_picture_filename: str | None
    curriculum_vitae_filename: str | None


class AlumniProfileOut(AlumniProfileBase):
    id: int
    account_id: int
    dean_approval_status: AlumniApprovalStatus
    employment_status: AlumniEmploymentStatus
    year_graduated: int
    address: str
    phone_number: str
    # socials: list
    course_id: int
    course: CourseOut
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class AlumniOccupationLocationIn(BaseModel):
    location: str