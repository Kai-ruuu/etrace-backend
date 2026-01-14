from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social import Social


class SocialRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, social: Social) -> Social:
        self.db.add(social)
        await self.db.flush()
        await self.db.refresh(social)
        return social
        
    
    async def get_by_id(self, id: int) -> Social | None:
        statement = select(Social).where(Social.id == id)
        result = await self.db.execute(statement)

        return result.scalar_one_or_none()
    

    async def get_by_name(self, name: str) -> Social | None:
        statement = select(Social).where(Social.name == name)
        result = await self.db.execute(statement)
        
        return result.scalar_one_or_none()
    

    async def get_all(self) -> list[Social]:
        statement = select(Social)
        result = await self.db.execute(statement)

        return result.scalars().all()
