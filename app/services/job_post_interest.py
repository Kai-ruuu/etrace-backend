from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.job_post_interest import JobPostInterestAlumniListOut, JobPostInterestCompanyListOut
from app.models.account import Account
from app.models.job_post_interest import JobPostInterest
from app.repositories.profile import ProfileRepository
from app.repositories.job_post import JobPostRepository
from app.repositories.job_post_interest import JobPostInterestRepository
from app.core.exceptions import *
from app.core.enums import Action
from app.core.enums import AccountRole


class JobPostInterestService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.job_post_repo = JobPostRepository(self.db)
        self.job_post_interest_repo = JobPostInterestRepository(self.db)
        self.alumni_profile_repo = ProfileRepository(self.db, AccountRole.ALUMNI)
        self.company_profile_repo = ProfileRepository(self.db, AccountRole.COMPANY)
    
    
    async def mark_as_reviewed(
        self,
        user: Account,
        job_post_interest_id: int,
        as_pymodel: bool = False
    ) -> JobPostInterest | JobPostInterestCompanyListOut:
        user.permissions.raise_unauthorized_if_excludes(Action.REVIEW_UNREVIEW_JOB_POST_INTERESTS)
        
        company_profile = await self.company_profile_repo.get_by_account_id(user.id)
        db_job_post_interest = await self.job_post_interest_repo.get_by_id_and_company_id(job_post_interest_id, company_profile.id)

        if not db_job_post_interest:
            raise JOB_POST_CV_SENDER_NOT_FOUND_EXCEPTION
        
        if db_job_post_interest.is_reviewed:
            raise JOB_POST_INTEREST_CV_ALREADY_REVIEWED_EXCEPTION
        
        updated_job_post_interest = await self.job_post_interest_repo.mark_as_reviewed(db_job_post_interest)
        return JobPostInterestCompanyListOut.model_validate(updated_job_post_interest) if as_pymodel else updated_job_post_interest
    
    
    async def mark_as_not_reviewed(
        self,
        user: Account,
        job_post_interest_id: int,
        as_pymodel: bool = False
    ) -> JobPostInterest | JobPostInterestCompanyListOut:
        user.permissions.raise_unauthorized_if_excludes(Action.REVIEW_UNREVIEW_JOB_POST_INTERESTS)
        
        company_profile = await self.company_profile_repo.get_by_account_id(user.id)
        db_job_post_interest = await self.job_post_interest_repo.get_by_id_and_company_id(job_post_interest_id, company_profile.id)

        if not db_job_post_interest:
            raise JOB_POST_CV_SENDER_NOT_FOUND_EXCEPTION
        
        if not db_job_post_interest.is_reviewed:
            raise JOB_POST_INTEREST_CV_ALREADY_NOT_REVIEWED_EXCEPTION
        
        updated_job_post_interest = await self.job_post_interest_repo.mark_as_not_reviewed(db_job_post_interest)
        return JobPostInterestCompanyListOut.model_validate(updated_job_post_interest) if as_pymodel else updated_job_post_interest


    async def get_alumni_list(self, user: Account, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_JOB_POST_INTERESTS)
        
        alumni_profile = await self.alumni_profile_repo.get_by_account_id(user.id)
        job_post_interests, total, total_pages = await self.job_post_interest_repo.get_alumni_list(alumni_profile.id, page, page_size)
        items = [JobPostInterestAlumniListOut.model_validate(job_post_interest) for job_post_interest in job_post_interests]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }


    async def get_company_list(self, user: Account, job_post_id: int, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_JOB_POST_INTERESTS)
        
        company_profile = await self.company_profile_repo.get_by_account_id(user.id)
        db_job_post = await self.job_post_repo.get_by_id_and_company_id(job_post_id, company_profile.id)

        if not db_job_post:
            raise JOB_POST_NOT_FOUND_EXCEPTION
        
        job_post_interests, total, total_pages = await self.job_post_interest_repo.get_company_list(job_post_id, page, page_size)
        items = [JobPostInterestCompanyListOut.model_validate(job_post_interest) for job_post_interest in job_post_interests]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }