from datetime import datetime
from pydantic import BaseModel, Field

from app.core.enums import JobPostWorkSetup, JobPostEmploymentType
from app.schemas.course import CourseOut
from app.schemas.company_profile import CompanyProfileOut


class JobPostBase(BaseModel):
    title: str
    description: str
    requirements: str
    responsibilities: str
    location: str
    application_steps: str
    work_setup: JobPostWorkSetup
    employment_type: JobPostEmploymentType
    salary_min: int
    salary_max: int
    is_payment_monthly: bool


class JobPostIn(JobPostBase):
    target_courses_ids: list[int]
    publish: bool = True


class JobPostOut(JobPostBase):
    id: int
    is_archived: bool
    is_published: bool
    company: CompanyProfileOut
    job_post_course: list[CourseOut] = []
    company_profile_id: int
    model_config = {"from_attributes": True}