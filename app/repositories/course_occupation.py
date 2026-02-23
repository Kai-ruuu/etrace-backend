from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, cast, String

from app.models.course_occupation import AlignedCourseAndOccupation


class AlignedCourseAndOccupationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    
    async def create(self, aligned_course_and_occupation: AlignedCourseAndOccupation) -> AlignedCourseAndOccupation:
        self.db.add(aligned_course_and_occupation)
        await self.db.flush()
        await self.db.refresh(aligned_course_and_occupation)
        return aligned_course_and_occupation
    
    
    async def get_by_course_and_occupation_id(self, course_id: int, occupation_id: int) -> AlignedCourseAndOccupation | None:
        statement = select(AlignedCourseAndOccupation).where(AlignedCourseAndOccupation.course_id == course_id, AlignedCourseAndOccupation.occupation_id == occupation_id)
        return (await self.db.execute(statement)).scalar_one_or_none()
    

    async def delete(self, aligned_course_and_occupation: AlignedCourseAndOccupation) -> AlignedCourseAndOccupation:
        await self.db.delete(aligned_course_and_occupation)
        return aligned_course_and_occupation