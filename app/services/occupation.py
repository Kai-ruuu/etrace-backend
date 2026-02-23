from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logging import Logger
from app.schemas.occupation import OccupationOut
from app.core.enums import Action
from app.core.exceptions import *
from app.core.enums import AccountRole
from app.models.account import Account
from app.models.occupation import Occupation
from app.models.course_occupation import AlignedCourseAndOccupation
from app.repositories.course import CourseRepository
from app.repositories.profile import ProfileRepository
from app.repositories.occupation import OccupationRepository
from app.repositories.course_occupation import AlignedCourseAndOccupationRepository


class OccupationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.course_repo = CourseRepository(self.db)
        self.occupation_repo = OccupationRepository(self.db)
        self.dean_profile_repo = ProfileRepository(self.db, AccountRole.DEAN)
        self.alignement_repo = AlignedCourseAndOccupationRepository(self.db)
        
    
    async def get_all(self, as_pymodel: bool = False) -> list[Occupation] | list[OccupationOut]:
        occupations = await self.occupation_repo.get_all()
        return [OccupationOut.model_validate(occupation) for occupation in occupations] if as_pymodel else occupations


    async def search_with_course_id(
        self,
        user: Account,
        course_id: int,
        aligned: bool | None = False,
        query: str | None = None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_OCCUPATIONS)

        db_dean_profile = await self.dean_profile_repo.get_by_account_id(user.id)

        if not db_dean_profile:
            raise UNAUTHORIZED_ACCESS_EXCEPION
        
        course_belongs_to_dean_school = await self.course_repo.get_belongs_to_dean_school(db_dean_profile.school_id, course_id)

        if not course_belongs_to_dean_school:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        occupations, total, total_pages = await self.occupation_repo.search_with_course_id(course_id, aligned, query, page, page_size)
        items = [OccupationOut.model_validate(occupation) for occupation in occupations]
        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        
    
    async def unalign_by_course_and_occupation_id(
        self,
        user: Account,
        course_id: int,
        occupation_id: int,
        as_pymodel: bool = False
    ) -> Occupation | OccupationOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ALIGN_UNALIGN_OCCUPATIONS)
        
        db_course = await self.course_repo.get_by_id(course_id)

        if not db_course:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        db_occupation = await self.occupation_repo.get_by_id(occupation_id)
        
        if not db_occupation:
            raise OCCUPATION_NOT_FOUND_EXCEPTION
        
        db_alignement = await self.alignement_repo.get_by_course_and_occupation_id(course_id, occupation_id)

        if not db_alignement:
            raise OCCUPATION_ALIGNMENT_NOT_FOUND_EXCEPTION
        
        try:
            await self.alignement_repo.delete(db_alignement)
            await self.db.commit()
            return OccupationOut.model_validate(db_occupation) if as_pymodel else db_occupation
        except SQLAlchemyError as e:
            await self.db.rollback()
            Logger.error(f"Unable to unalign occupation. - {repr(e)}")
            raise OCCUPATION_UNABLE_TO_UNALIGN_EXCEPTION
    

    async def align_by_course_and_occupation_id(
        self,
        user: Account,
        course_id: int,
        occupation_id: int,
        as_pymodel: bool = False
    ) -> Occupation | OccupationOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ALIGN_UNALIGN_OCCUPATIONS)

        db_course = await self.course_repo.get_by_id(course_id)

        if not db_course:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        db_occupation = await self.occupation_repo.get_by_id(occupation_id)
        
        if not db_occupation:
            raise OCCUPATION_NOT_FOUND_EXCEPTION
        
        db_alignement = await self.alignement_repo.get_by_course_and_occupation_id(course_id, occupation_id)

        if db_alignement:
            raise OCCUPATION_ALREADY_ALIGNED_EXCEPTION
        
        try:
            await self.alignement_repo.create(AlignedCourseAndOccupation(
                course_id=course_id,
                occupation_id=occupation_id
            ))
            await self.db.commit()
            return OccupationOut.model_validate(db_occupation) if as_pymodel else db_occupation
        except SQLAlchemyError as e:
            await self.db.rollback()
            Logger.error(f"Unable to align occupation to course.")
            raise OCCUPATION_UNABLE_TO_ALIGN_EXCEPTION