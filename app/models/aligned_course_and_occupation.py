from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base

class AlignedCourseAndOccupation(Base):
    __tablename__ = "aligned_occupations"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = Column(Integer, ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship("Course", back_populates="aligned_course_and_occupations") # type: ignore
    occupation_id: Mapped[int] = Column(Integer, ForeignKey("occupations.id"))
    occupation: Mapped["Occupation"] = relationship("Occupation", back_populates="aligned_course_and_occupations") # type: ignore

