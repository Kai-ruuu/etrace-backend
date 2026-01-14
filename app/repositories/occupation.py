from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.occupation import Occupation


class OccupationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        
    
    async def create(self, occupation: Occupation) -> Occupation:
        self.db.add(occupation)
        await self.db.flush()
        await self.db.refresh(occupation)
        return occupation

    
    async def get_or_create_by_title(self, title: str) -> Occupation:
        normalized_title = title.strip().lower()

        existing = await self.get_by_normalized_title(normalized_title)
        if existing:
            return existing

        occupation = Occupation(
            title=title,
            normalized_title=normalized_title
        )
        self.db.add(occupation)
        await self.db.flush()
        await self.db.refresh(occupation)
        return occupation
    
    async def get_by_id(self, id: int) -> Occupation | None:
        statement = select(Occupation).where(Occupation.id == id)
        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
    

    async def get_by_title(self, title: str) -> Occupation | None:
        statement = select(Occupation).where(Occupation.title == title)
        result = await self.db.execute(statement)
        
        return result.scalar_one_or_none()

    async def get_by_normalized_title(self, normalized_title: str) -> Occupation | None:
        statement = select(Occupation).where(Occupation.normalized_title == normalized_title)
        result = await self.db.execute(statement)
        
        return result.scalar_one_or_none()
    

    async def get_all(self) -> list[Occupation]:
        statement = select(Occupation)
        result = await self.db.execute(statement)

        return result.scalars().all()
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[Occupation], int, int]:
        base_statement = select(Occupation)
        count_statement = select(func.count()).select_from(Occupation)

        if query:
            search_filter = Occupation.title.ilike(f"%{query}%")
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)
        
        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size
        
        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        occupations = result.scalars().unique().all()

        return occupations, total, total_pages


    