from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_, cast, String

from app.utils.datetime import get_utc_now
from app.models.job_post import JobPost
from app.models.job_post_course import JobPostCourse
from app.models.company_profile import CompanyProfile


class JobPostRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, job_post: JobPost) -> JobPost:
        self.db.add(job_post)
        await self.db.flush()
        await self.db.refresh(job_post)
        return job_post
        
    
    async def get_by_id(self, id: int) -> JobPost | None:
        statement = (
            select(JobPost)
            .where(JobPost.id == id)
            .options(
                selectinload(JobPost.company),
                selectinload(JobPost.job_post_courses)
            )
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    
    
    async def get_by_id_and_company_id(self, id: int, company_id: int) -> bool:
        statement = (
            select(JobPost)
            .where(
                JobPost.id == id,
                JobPost.company_profile_id == company_id
            )
        )
        return (await self.db.execute(statement)).scalar_one_or_none()
    

    # [mark] for existence check only
    async def get_by_title_and_company_profile_id(self, job_title: str, company_profile_id: int) -> JobPost | None:
        statement = select(JobPost).where(
            JobPost.company_profile_id == company_profile_id,
            JobPost.normalized_title == job_title.strip().lower()
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    async def get_all(self) -> list[JobPost]:
        statement = (
            select(JobPost)
            .options(
                selectinload(JobPost.company),
                selectinload(JobPost.job_post_courses)
            )
        )
        result = await self.db.execute(statement)
        return result.scalars().all()
    
    
    # [mark] primarily used by alumni
    async def get_by_latest(self, user_course_id: int, page: int = 1, page_size: int = 20) -> tuple[list[JobPost], int, int]:
        search_filter = and_(
            JobPost.is_archived.is_(False),
            JobPost.is_published.is_(True),
            JobPostCourse.job_post_course_id == user_course_id
        )

        base_statement = (
            select(JobPost)
            .options(
                selectinload(JobPost.company),
                selectinload(JobPost.job_post_courses),
            )
            .join(JobPost.job_post_courses)
            .where(search_filter)
            .order_by(JobPost.posted_at.desc())
        )

        count_statement = (
            select(func.count(func.distinct(JobPost.id)))
            .select_from(JobPost)
            .join(JobPost.job_post_courses)
            .where(search_filter)
        )

        total = (await self.db.execute(count_statement)).scalar()
        total_pages = (total + page_size - 1) // page_size

        result = await self.db.execute(
            base_statement
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        job_posts = result.scalars().unique().all()
        return job_posts, total, total_pages
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[JobPost], int, int]:
        base_statement = (
            select(JobPost)
            .options(
                selectinload(JobPost.company),
                selectinload(JobPost.job_post_courses)
            )
        )
        count_statement = select(func.count()).select_from(JobPost)

        if query:
            search_filter = or_(
                JobPost.title.ilike(f"%{query}%"),
                JobPost.location.ilike(f"%{query}%"),
                cast(JobPost.work_setup, String).ilike(f"%{query}%"),
                cast(JobPost.employment_type, String).ilike(f"%{query}%"),
                cast(JobPost.salary_min, String).ilike(f"%{query}%"),
                cast(JobPost.salary_max, String).ilike(f"%{query}%"),
            )
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)
        
        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size
        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        job_posts = result.scalars().unique().all()
        return job_posts, total, total_pages
    

    async def archive(self, db_job_post: JobPost) -> JobPost:
        db_job_post.is_archived = True
        await self.db.commit()
        await self.db.refresh(db_job_post, attribute_names=["company", "job_post_courses"])
        return db_job_post
    

    async def restore(self, db_job_post: JobPost) -> JobPost:
        db_job_post.is_archived = False
        await self.db.commit()
        await self.db.refresh(db_job_post, attribute_names=["company", "job_post_courses"])
        return db_job_post
    

    async def unpublish(self, db_job_post: JobPost) -> JobPost:
        db_job_post.is_published = False
        await self.db.commit()
        await self.db.refresh(db_job_post, attribute_names=["company", "job_post_courses"])
        return db_job_post
    

    async def publish(self, db_job_post: JobPost) -> JobPost:
        db_job_post.is_published = True
        db_job_post.posted_at = get_utc_now()
        await self.db.commit()
        await self.db.refresh(db_job_post, attribute_names=["company", "job_post_courses"])
        return db_job_post