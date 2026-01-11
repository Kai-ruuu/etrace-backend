from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, literal

from app.models.school import School


class SchoolRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, school: School) -> School:
        self.db.add(school)
        await self.db.flush()
        await self.db.refresh(school)
        return school
        
    
    async def get_by_id(self, id: int) -> School | None:
        statement = select(School).where(School.id == id)
        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
    

    async def get_by_name(self, name: str) -> School | None:
        statement = select(School).where(School.name == name)
        result = await self.db.execute(statement)
        
        return result.scalar_one_or_none()
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[School], int, int]:
        base_statement = select(School)
        count_statement = select(func.count()).select_from(School)

        if query:
            search_filter = School.name.ilike(f"%{query}%")
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)
        
        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size
        
        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        schools = result.scalars().unique().all()

        return schools, total, total_pages
    

    async def archive(self, db_school: School) -> School:
        db_school.is_archived = True
        
        await self.db.commit()
        await self.db.refresh(db_school)
        return db_school
    

    async def restore(self, db_school: School) -> School:
        db_school.is_archived = False
        
        await self.db.commit()
        await self.db.refresh(db_school)
        return db_school


    