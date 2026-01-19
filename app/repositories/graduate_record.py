from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.graduate_record import GraduateRecord


class GraduateRecordRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, graduate_record: GraduateRecord) -> GraduateRecord:
        self.db.add(graduate_record)
        await self.db.flush()
        await self.db.refresh(graduate_record)
        return graduate_record
        
    
    async def get_by_id(self, id: int) -> GraduateRecord | None:
        statement = select(GraduateRecord).where(GraduateRecord.id == id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    async def get_by_filename(self, filename: str) -> GraduateRecord | None:
        statement = select(GraduateRecord).where(GraduateRecord.record_filename == filename.strip().lower())
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    async def get_all(self) -> list[GraduateRecord]:
        statement = select(GraduateRecord)
        result = await self.db.execute(statement)
        return result.scalars().all()
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[GraduateRecord], int, int]:
        base_statement = select(GraduateRecord)
        count_statement = select(func.count()).select_from(GraduateRecord)

        if query:
            search_filter = GraduateRecord.record_filename.ilike(f"%{query}%")
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)
        
        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size
        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        graduate_records = result.scalars().unique().all()
        return graduate_records, total, total_pages
    

    async def archive(self, db_graduate_record: GraduateRecord) -> GraduateRecord:
        db_graduate_record.is_archived = True
        await self.db.commit()
        await self.db.refresh(db_graduate_record)
        return db_graduate_record
    

    async def restore(self, db_graduate_record: GraduateRecord) -> GraduateRecord:
        db_graduate_record.is_archived = False
        await self.db.commit()
        await self.db.refresh(db_graduate_record)
        return db_graduate_record


    