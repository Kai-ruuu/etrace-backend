from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, cast, String

from app.models.job_post import JobPost
from app.models.company_profile import CompanyProfile
from app.models.job_post_interest import JobPostInterest


class JobPostInterestRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, job_post_interest: JobPostInterest) -> JobPostInterest:
        self.db.add(job_post_interest)
        await self.db.flush()
        await self.db.refresh(job_post_interest)
        return job_post_interest
    

    async def get_by_id_and_company_id(self, id: int, company_id: int) -> JobPostInterest | None:
        statement = (
            select(JobPostInterest)
            .join(JobPostInterest.job_post)
            .join(JobPost.company)
            .where(
                JobPostInterest.id == id,
                CompanyProfile.id == company_id
            )
        )
        return (await self.db.execute(statement)).scalar_one_or_none()
    
    
    async def get_by_job_post_and_alumni_id(self, job_post_id: int, alumni_id: int) -> JobPostInterest | None:
        statement = (
            select(JobPostInterest)
            .where(
                JobPostInterest.job_post_id == job_post_id,
                JobPostInterest.alumni_profile_id == alumni_id
            )
        )
        return (await self.db.execute(statement)).scalar_one_or_none()
    
    
    # [mark] for alumni only
    async def get_alumni_list(self, alumni_id: int, page: int = 1, page_size: int = 20) -> tuple[list[JobPostInterest], int, int]:
        search_filter = JobPostInterest.alumni_profile_id == alumni_id

        base_statement = (
            select(JobPostInterest)
            .join(JobPostInterest.job_post)
            .join(JobPost.company)
            .options(
                selectinload(JobPostInterest.job_post)
                .selectinload(JobPost.company)
            )
            .where(search_filter)
            .order_by(JobPostInterest.created_at.desc())
        )

        count_statement = (
            select(func.count(func.distinct(JobPostInterest.id)))
            .select_from(JobPostInterest)
            .where(search_filter)
        )

        total = (await self.db.execute(count_statement)).scalar()
        total_pages = (total + page_size - 1) // page_size

        result = await self.db.execute(
            base_statement
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        job_post_interests = result.scalars().unique().all()
        return job_post_interests, total, total_pages
    
    
    # [mark] for companies only
    async def get_company_list(self, job_post_id: int, page: int = 1, page_size: int = 20) -> tuple[list[JobPostInterest], int, int]:
        search_filter = JobPostInterest.job_post_id == job_post_id

        base_statement = (
            select(JobPostInterest)
            .options(
                selectinload(JobPostInterest.alumni),
            )
            .where(search_filter)
            .order_by(JobPostInterest.created_at.desc())
        )

        count_statement = (
            select(func.count(func.distinct(JobPostInterest.id)))
            .select_from(JobPostInterest)
            .where(search_filter)
        )

        total = (await self.db.execute(count_statement)).scalar()
        total_pages = (total + page_size - 1) // page_size

        result = await self.db.execute(
            base_statement
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        job_post_interests = result.scalars().unique().all()
        return job_post_interests, total, total_pages
    
    # [mark] for companies only
    async def mark_as_reviewed(self, job_post_interest: JobPostInterest) -> JobPostInterest:
        job_post_interest.is_reviewed = True
        await self.db.commit()
        await self.db.refresh(job_post_interest, attribute_names=["alumni"])
        return job_post_interest
    
    # [mark] for companies only
    async def mark_as_not_reviewed(self, job_post_interest: JobPostInterest) -> JobPostInterest:
        job_post_interest.is_reviewed = False
        await self.db.commit()
        await self.db.refresh(job_post_interest, attribute_names=["alumni"])
        return job_post_interest