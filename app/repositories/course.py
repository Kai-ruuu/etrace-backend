from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course


class CourseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.flush()
        await self.db.refresh(course)
        return course
        
    
    async def get_by_id(self, id: int) -> Course | None:
        statement = select(Course).where(Course.id == id)
        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
    

    async def get_by_name(self, name: str) -> Course | None:
        statement = select(Course).where(Course.normalized_name == name.strip().lower())
        result = await self.db.execute(statement)
        
        return result.scalar_one_or_none()
    

    async def get_all(self) -> list[Course]:
        statement = select(Course)
        result = await self.db.execute(statement)

        return result.scalars().all()
    
    
    # [mark] for existence check only
    async def get_batch_exists(self, ids: list[int]) -> tuple[bool, list]:
        statement = select(Course.id).where(Course.id.in_(ids))
        result = await self.db.execute(statement)
        found_ids = set(result.scalars().all())
        missing_ids = set(ids) - found_ids
        return len(missing_ids) == 0, list(missing_ids)
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[Course], int, int]:
        base_statement = select(Course)
        count_statement = select(func.count()).select_from(Course)

        if query:
            search_filter = Course.normalized_name.ilike(f"%{query}%")
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)
        
        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size
        
        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        courses = result.scalars().unique().all()

        return courses, total, total_pages
    

    async def archive(self, db_course: Course) -> Course:
        db_course.is_archived = True
        
        await self.db.commit()
        await self.db.refresh(db_course)
        return db_course
    

    async def restore(self, db_course: Course) -> Course:
        db_course.is_archived = False
        
        await self.db.commit()
        await self.db.refresh(db_course)
        return db_course


    