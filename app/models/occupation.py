from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String

from app.database import Base

class Occupation(Base):
    __tablename__ = "occupations"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    occupation_states: Mapped[list["OccupationState"]] = relationship("OccupationState", back_populates="occupation", uselist=True, cascade="all, delete-orphan") # type: ignore
    aligned_course_and_occupations: Mapped[list["AlignedCourseAndOccupation"]] = relationship("AlignedCourseAndOccupation", back_populates="occupation") # type: ignore
