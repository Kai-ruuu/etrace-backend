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


    