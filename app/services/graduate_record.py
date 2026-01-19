from fastapi import UploadFile, Form, File
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.graduate_record import GraduateRecordOut
from app.repositories.graduate_record import GraduateRecordRepository
from app.core.exceptions import *
from app.core.enums import Action
from app.models.account import Account
from app.models.graduate_record import GraduateRecord
from app.utils.logging import Logger
from app.utils.storage import Upload, UploadManager, DestFolder
from app.utils.validation import validate_and_transform_graduate_record


class GraduateRecordService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = GraduateRecordRepository(self.db)
        self.upload_manager = UploadManager()


    async def create(
        self,
        user: Account,
        graduate_record_file: UploadFile | None = File(None),
        graduation_year: int = Form(...),
        course_id: int = Form(...),
        as_pymodel: bool = False
    ) -> GraduateRecord | GraduateRecordOut:
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_GRADUATE_RECORDS)

        # stage file
        await self.upload_manager.stage_uploads([Upload(file=graduate_record_file, dest_folder=DestFolder.RECORD, allowed_mimes={"text/csv"})])

        # check csv structure validity
        temp_file_path = self.upload_manager.get_staged_file_path(DestFolder.RECORD)

        # validate and transform csv file contents
        await validate_and_transform_graduate_record(temp_file_path, self.upload_manager)

        try:
            graduate_record = await self.repo.create(GraduateRecord(
                record_filename=self.upload_manager.get_staged_file_name(DestFolder.RECORD),
                graduation_year=graduation_year,
                course_id=course_id
            ))
            await self.db.commit()
            await self.db.refresh(graduate_record)
            
            # save the transformed csv file
            await self.upload_manager.commit()
            
            return GraduateRecordOut.model_validate(graduate_record) if as_pymodel else graduate_record
        except HTTPException:
            await self.upload_manager.rollback()
            raise
        except IntegrityError as e:
            Logger.error(f"Unable to create Graduate Record - {repr(e)}")
            
            match e.orig.args[0]:
                case 1062:
                    raise GRADUATE_RECORD_ALREADY_EXISTS_EXCEPTION
                case _:
                    raise UNABLE_TO_CREATE_GRADUATE_RECORD_EXCEPTION
        except Exception as e:
            await self.upload_manager.rollback()
            Logger.error(f"Unable to create Graduate Record - {repr(e)}")
            RAISE_FILE_CANNOT_BE_READ_EXCEPTION(DestFolder.RECORD.value)
            
    
    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> GraduateRecord | GraduateRecordOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_GRADUATE_RECORDS)
        
        db_school = await self.repo.get_by_id(id)

        if not db_school:
            raise GRADUATE_RECORD_NOT_FOUND_EXCEPTION
        
        return GraduateRecordOut.model_validate(db_school) if as_pymodel else db_school

    
    async def get_by_name(self, user: Account, name: str, as_pymodel: bool = False) -> GraduateRecord | GraduateRecordOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_GRADUATE_RECORDS)

        db_school = await self.repo.get_by_name(name)

        if not db_school:
            raise GRADUATE_RECORD_NOT_FOUND_EXCEPTION
        
        return GraduateRecordOut.model_validate(db_school) if as_pymodel else db_school
    
    
    async def search(self, user: Account, query: str, page: int = 1, page_size: int = 20) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_GRADUATE_RECORDS)
        
        schools, total, total_pages = await self.repo.search(query, page,  page_size)

        items = [GraduateRecordOut.model_validate(school) for school in schools]

        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    
    async def archive_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> GraduateRecord | GraduateRecordOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_GRADUATE_RECORDS)

        db_school = await self.repo.get_by_id(id)

        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION
        
        if db_school.is_archived:
            raise GRADUATE_RECORD_ALREADY_ARCHIVED_EXCEPTION
        
        db_school = await self.repo.archive(db_school)
        
        return GraduateRecordOut.model_validate(db_school) if as_pymodel else db_school

    
    async def restore_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> GraduateRecord | GraduateRecordOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ARCHIVE_RESTORE_GRADUATE_RECORDS)

        db_school = await self.repo.get_by_id(id)

        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION
        
        if not db_school.is_archived:
            raise GRADUATE_RECORD_ALREADY_RESTORED_EXCEPTION
        
        db_school = await self.repo.restore(db_school)
        
        return GraduateRecordOut.model_validate(db_school) if as_pymodel else db_school