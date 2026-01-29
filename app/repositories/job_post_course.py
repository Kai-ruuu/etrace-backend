from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, cast, String

from app.models.job_post_course import JobPostCourse


class JobPostCourseCourseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, job_post_course: JobPostCourse) -> JobPostCourse:
        self.db.add(job_post_course)
        await self.db.flush()
        await self.db.refresh(job_post_course)
        return job_post_course
        
    
    async def get_by_id(self, id: int) -> JobPostCourse | None:
        statement = select(JobPostCourse).where(JobPostCourse.id == id)
        return (await self.db.execute(statement)).scalar_one_or_none()
    

    # [mark] add delete feature