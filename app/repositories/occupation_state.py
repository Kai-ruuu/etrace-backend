from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.occupation_state import OccupationState


class OccupationStateRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, occupation_state: OccupationState) -> OccupationState:
        self.db.add(occupation_state)
        await self.db.flush()
        await self.db.refresh(occupation_state)
        return occupation_state
        
    
    async def get_by_id(self, id: int) -> OccupationState | None:
        statement = select(OccupationState).where(OccupationState.id == id)
        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
    

    async def get_all(self) -> list[OccupationState]:
        statement = select(OccupationState)
        result = await self.db.execute(statement)

        return result.scalars().all()
    

    async def search(self, query: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[OccupationState], int, int]:
        base_statement = select(OccupationState)
        count_statement = select(func.count()).select_from(OccupationState)

        if query:
            search_filter = OccupationState.title.ilike(f"%{query}%")
            base_statement = base_statement.where(search_filter)
            count_statement = count_statement.where(search_filter)
        
        total_result = await self.db.execute(count_statement)
        total = total_result.scalar()
        total_pages = (total + page_size - 1) // page_size
        
        search_statement = base_statement.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(search_statement)
        occupation_states = result.scalars().unique().all()

        return occupation_states, total, total_pages


    