from datetime import datetime
from pydantic import BaseModel

from app.schemas.job_post import JobPostOut
from app.schemas.alumni_profile import AlumniProfileOut


class JobPostInterestBase(BaseModel):
    id: int
    job_post_id: int
    alumni_profile_id: int


class JobPostInterestAlumniListOut(JobPostInterestBase):
    job_post: JobPostOut
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class JobPostInterestCompanyListOut(JobPostInterestBase):
    alumni: AlumniProfileOut
    created_at: datetime
    updated_at: datetime
    is_reviewed: bool
    model_config = {"from_attributes": True}