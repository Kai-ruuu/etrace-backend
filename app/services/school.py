from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logging import Logger
from app.schemas.school import SchoolIn, SchoolOut
from app.repositories.school import SchoolRepository
from app.core.exceptions import *
from app.core.enums import Action
from app.models.school import School
from app.models.account import Account
from app.models.system_admin_profile import SystemAdminProfile


class SchoolService:
    def __init__(self, db: AsyncSession, repo: SchoolRepository) -> None:
        self.db = db
        self.repo = repo


    async def create(self, user: Account, school: SchoolIn, as_pymodel: bool = False) -> School | SchoolOut:
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_SCHOOLS)
        
        try:
            db_school = await self.repo.get_by_name(school.name)

            if db_school:
                raise SCHOOL_ALREADY_EXISTS_EXCEPTION
            
            new_school = await self.repo.create(School(name=school.name))

            await self.db.commit()
            await self.db.refresh(new_school)
            return SchoolOut.model_validate(new_school) if as_pymodel else new_school
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to create school. - {repr(e)}")
            raise UNABLE_TO_CREATE_SCHOOL_EXCEPTION

    
    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> School | SchoolOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_SCHOOLS)
        
        db_school = await self.repo.get_by_id(id)

        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION
        
        return SchoolOut.model_validate(db_school) if as_pymodel else db_school

    
    async def get_by_name(self, user: Account, name: str, as_pymodel: bool = False) -> School | SchoolOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_SCHOOLS)

        db_school = await self.repo.get_by_name(name)

        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION
        
        return SchoolOut.model_validate(db_school) if as_pymodel else db_school
    
    
    async def search(self, user: Account, query: str, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_SCHOOLS)
        
        schools, total, total_pages = await self.repo.search(query, page,  page_size)

        items = [SchoolOut.model_validate(school) for school in schools]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    
    async def archive_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> School | SchoolOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_SCHOOLS)

        db_school = await self.repo.get_by_id(id)


        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION
        
        if db_school.is_archived:
            raise SCHOOL_ALREADY_ARCHIVED_EXCEPTION
        
        db_school = await self.repo.archive(db_school)
        
        return SchoolOut.model_validate(db_school) if as_pymodel else db_school

    
    async def restore_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> School | SchoolOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_SCHOOLS)

        db_school = await self.repo.get_by_id(id)


        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION
        
        if not db_school.is_archived:
            raise SCHOOL_ALREADY_RESTORED_EXCEPTION
        
        db_school = await self.repo.restore(db_school)
        
        return SchoolOut.model_validate(db_school) if as_pymodel else db_school