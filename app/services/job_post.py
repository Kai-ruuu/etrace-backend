from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logging import Logger
from app.schemas.job_post import JobPostIn, JobPostOut
from app.core.exceptions import *
from app.core.enums import Action, AccountRole, CompanyApprovalStatus
from app.models.account import Account
from app.models.job_post import JobPost
from app.models.job_post_like import JobPostLike
from app.models.job_post_course import JobPostCourse
from app.repositories.course import CourseRepository
from app.repositories.profile import ProfileRepository
from app.repositories.job_post import JobPostRepository
from app.repositories.job_post_like import JobPostLikeRepository
from app.repositories.job_post_course import JobPostCourseCourseRepository


class JobPostService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.course_repo = CourseRepository(self.db)
        self.job_post_repo = JobPostRepository(self.db)
        self.job_post_like_repo = JobPostLikeRepository(self.db)
        self.job_post_course_repo = JobPostCourseCourseRepository(self.db)
        self.alumni_profile_repo = ProfileRepository(self.db, AccountRole.ALUMNI)
        self.company_profile_repo = ProfileRepository(self.db, AccountRole.COMPANY)


    async def create(
        self,
        user: Account,
        job_post: JobPostIn,
        as_pymodel: bool = False
    ) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_JOB_POSTS)

        db_company_profile = await self.company_profile_repo.get_by_account_id(user.id)
        
        try:
            # verify if the job post does not exists yet wit the provided title and company profile id
            db_job_post = await self.job_post_repo.get_by_title_and_company_profile_id(job_post.title, db_company_profile.id)

            if db_job_post:
                raise JOB_POST_ALREADY_EXISTS_EXCEPTION

            if not db_company_profile:
                raise COMPANY_PROFILE_NOT_FOUND_EXCEPTION
            
            if (
                not db_company_profile.sysad_approval_status == CompanyApprovalStatus.APPROVED or
                not db_company_profile.peso_staff_approval_status == CompanyApprovalStatus.APPROVED
            ):
                raise COMPANY_NOT_FULLY_APPROVED_EXCEPTION
            
            # verify if all courses exists with the provided target course ids
            all_courses_exists, missing_ids = await self.course_repo.get_batch_exists(job_post.target_courses_ids)
            
            if not all_courses_exists:
                RAISE_COURSES_NOT_FOUND_BY_IDS(missing_ids)

            # create job post
            new_job_post = await self.job_post_repo.create(JobPost(
                title=job_post.title.strip(),
                normalized_title=job_post.title.strip().lower(),
                description=job_post.description,
                requirements=job_post.requirements,
                responsibilities=job_post.responsibilities,
                location=job_post.location,
                application_steps=job_post.application_steps,
                work_setup=job_post.work_setup,
                employment_type=job_post.employment_type,
                salary_min=job_post.salary_min,
                salary_max=job_post.salary_max,
                is_payment_monthly=job_post.is_payment_monthly,
                company_profile_id=db_company_profile.id,
                is_published=job_post.publish
            ))
            
            # create target course linkage
            for course_id in job_post.target_courses_ids:
                await self.job_post_course_repo.create(JobPostCourse(
                    job_post_id=new_job_post.id,
                    job_post_course_id=course_id
                ))

            await self.db.commit()
            await self.db.refresh(new_job_post, attribute_names=["company", "job_post_courses"])
            return JobPostOut.model_validate(new_job_post) if as_pymodel else new_job_post
        except HTTPException as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to creat job post. - {repr(e)}")
            raise UNABLE_TO_CREATE_JOB_POST_EXCEPTION
            
    
    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_JOB_POSTS)
        
        db_job_post = await self.job_post_repo.get_by_id(id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post

    
    async def get_by_latest(self, user: Account, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_JOB_POSTS)

        db_alumni_profile = await self.alumni_profile_repo.get_by_account_id(user.id)
        job_posts, total, total_pages = await self.job_post_repo.get_by_latest(db_alumni_profile.course_id, page, page_size)

        items = [JobPostOut.model_validate(job_post) for job_post in job_posts]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    
    async def search(self, user: Account, query: str, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_JOB_POSTS)
        
        job_posts, total, total_pages = await self.job_post_repo.search(query, page,  page_size)

        items = [JobPostOut.model_validate(job_post) for job_post in job_posts]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    
    async def archive_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_JOB_POSTS)

        db_job_post = await self.job_post_repo.get_by_id(id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        if db_job_post.is_archived:
            raise JOB_POST_ALREADY_ARCHIVED_EXCEPTION
        
        if db_job_post.is_published:
            raise JOB_POST_ARCHIVE_PUBLISHED_EXCEPTION
        
        db_job_post = await self.job_post_repo.archive(db_job_post)
        
        return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post

    
    async def restore_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_JOB_POSTS)

        db_job_post = await self.job_post_repo.get_by_id(id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        if not db_job_post.is_archived:
            raise JOB_POST_ALREADY_RESTORED_EXCEPTION
        
        db_job_post = await self.job_post_repo.restore(db_job_post)
        
        return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post

    
    async def unpublish_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.PUBLISH_UNPUBLISH_JOB_POSTS)

        db_job_post = await self.job_post_repo.get_by_id(id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        if db_job_post.is_archived:
            raise JOB_POST_UNPUBLISH_ARCHIVED_EXCEPTION
        
        if not db_job_post.is_published:
            raise JOB_POST_ALREADY_UNPUBLISHED_EXCEPTION
        
        # [mark] delete job post likes
        db_job_post = await self.job_post_repo.unpublish(db_job_post)
        
        return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post

    
    async def publish_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.PUBLISH_UNPUBLISH_JOB_POSTS)

        db_job_post = await self.job_post_repo.get_by_id(id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        if db_job_post.is_archived:
            raise JOB_POST_PUBLISH_ARCHIVED_EXCEPTION

        if db_job_post.is_published:
            raise JOB_POST_ALREADY_PUBLISHED_EXCEPTION
        
        db_job_post = await self.job_post_repo.publish(db_job_post)
        
        return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post
    

    async def dislike(self, user: Account, job_post_id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.LIKE_DISLIKE_JOB_POSTS)

        db_job_post = await self.job_post_repo.get_by_id(job_post_id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        db_alumni_profile = await self.alumni_profile_repo.get_by_account_id(user.id)
        db_job_post_like = await self.job_post_like_repo.get_by_job_post_and_alumni_id(job_post_id, db_alumni_profile.id)
        
        if not db_job_post_like:
            raise JOB_POST_LIKE_NOT_FOUND_EXCEPTION
        
        try:
            await self.job_post_like_repo.delete(db_job_post_like)
            await self.db.commit()
            return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post
        except SQLAlchemyError as e:
            await self.db.rollback()
            Logger.error(f"Unable to dislike job post. - {repr(e)}")
            raise JOB_POST_UNABLE_TO_DISLIKE_EXCEPTION
    

    async def like(self, user: Account, job_post_id: int, as_pymodel: bool = False) -> JobPost | JobPostOut:
        user.permissions.raise_unauthorized_if_excludes(Action.LIKE_DISLIKE_JOB_POSTS)

        db_job_post = await self.job_post_repo.get_by_id(job_post_id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        db_alumni_profile = await self.alumni_profile_repo.get_by_account_id(user.id)
        
        try:
            await self.job_post_like_repo.create(JobPostLike(
                job_post_id=job_post_id,
                alumni_profile_id=db_alumni_profile.id
            ))
            await self.db.commit()
            return JobPostOut.model_validate(db_job_post) if as_pymodel else db_job_post
        except SQLAlchemyError as e:
            await self.db.rollback()
            Logger.error(f"Unable to like job post. - {repr(e)}")
            raise JOB_POST_UNABLE_TO_DISLIKE_EXCEPTION