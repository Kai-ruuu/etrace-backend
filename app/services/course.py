from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logging import Logger
from app.schemas.course import CourseIn, CourseOut
from app.repositories.course import CourseRepository
from app.repositories.profile import ProfileRepository
from app.core.exceptions import *
from app.core.enums import Action
from app.models.course import Course
from app.models.account import Account


class CourseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = CourseRepository(self.db)


    async def create(self, user: Account, course: CourseIn, as_pymodel: bool = False) -> Course | CourseOut:
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_COURSES)

        try:
            db_course = await self.repo.get_by_name(course.name)

            if db_course:
                raise COURSE_ALREADY_EXISTS_EXCEPTION
            
            new_course = await self.repo.create(Course(
                name=course.name,
                normalized_name=course.name.strip().lower(),
                school_id=course.school_id
            ))

            await self.db.commit()
            await self.db.refresh(new_course)
            return CourseOut.model_validate(new_course) if as_pymodel else new_course
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to create course. - {repr(e)}")
            raise UNABLE_TO_CREATE_COURSE_EXCEPTION


    async def get_all(self, as_pymodel: bool = False) -> list[Course] | list[CourseOut]:
        # user.permissions.raise_unauthorized_if_excludes(Action.READ_COURSES)
        
        courses = await self.repo.get_all()
        return [CourseOut.model_validate(course) for course in courses] if as_pymodel else courses

    
    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Course | CourseOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COURSES)
        
        db_course = await self.repo.get_by_id(id)

        if not db_course:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        return CourseOut.model_validate(db_course) if as_pymodel else db_course
    
    
    async def get_dean_list(self, user: Account, as_pymodel: bool = False) -> list[Course] | list[CourseOut]:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COURSES)

        dean_profile_repo = ProfileRepository(self.db, user.role)
        db_dean_profile = await dean_profile_repo.get_by_account_id(user.id)
        
        if not db_dean_profile:
            raise UNAUTHORIZED_ACCESS_EXCEPION
        
        db_dean_school_courses = await self.repo.get_by_school_id(db_dean_profile.school_id)
        
        return [CourseOut.model_validate(course) for course in db_dean_school_courses] if as_pymodel else db_dean_school_courses
    
    async def get_by_name(self, user: Account, name: str, as_pymodel: bool = False) -> Course | CourseOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COURSES)

        db_course = await self.repo.get_by_name(name)

        if not db_course:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        return CourseOut.model_validate(db_course) if as_pymodel else db_course
    
    
    async def search(self, user: Account, query: str | None, archived: bool | None, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_COURSES)
        
        courses, total, total_pages = await self.repo.search(query, archived, page, page_size)

        items = [CourseOut.model_validate(course) for course in courses]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    
    async def archive_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Course | CourseOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_COURSES)

        db_course = await self.repo.get_by_id(id)


        if not db_course:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        if db_course.is_archived:
            raise COURSE_ALREADY_ARCHIVED_EXCEPTION
        
        db_course = await self.repo.archive(db_course)
        
        return CourseOut.model_validate(db_course) if as_pymodel else db_course

    
    async def restore_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Course | CourseOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_COURSES)

        db_course = await self.repo.get_by_id(id)


        if not db_course:
            raise COURSE_NOT_FOUND_EXCEPTION
        
        if not db_course.is_archived:
            raise COURSE_ALREADY_RESTORED_EXCEPTION
        
        db_course = await self.repo.restore(db_course)
        
        return CourseOut.model_validate(db_course) if as_pymodel else db_course

