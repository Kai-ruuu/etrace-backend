from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, cast, String

from app.models.job_post_like import JobPostLike


class JobPostLikeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, job_post_like: JobPostLike) -> JobPostLike:
        self.db.add(job_post_like)
        await self.db.flush()
        await self.db.refresh(job_post_like)
        return job_post_like
    
    
    async def get_by_job_post_and_alumni_id(self, job_post_id: int, alumni_id: int) -> JobPostLike | None:
        statement = select(JobPostLike).where(JobPostLike.job_post_id == job_post_id, JobPostLike.alumni_profile_id == alumni_id)
        return (await self.db.execute(statement)).scalar_one_or_none()
    

    async def delete(self, job_post_like: JobPostLike) -> JobPostLike:
        await self.db.delete(job_post_like)
        return job_post_like