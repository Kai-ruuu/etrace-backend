from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, cast, String

from app.models.job_post_course import JobPostCourse


class JobPostCourseCourseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, job_post: JobPostCourse) -> JobPostCourse:
        self.db.add(job_post)
        await self.db.flush()
        await self.db.refresh(job_post)
        return job_post
        
    
    async def get_by_id(self, id: int) -> JobPostCourse | None:
        statement = select(JobPostCourse).where(JobPostCourse.id == id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    # [mark] add delete feature