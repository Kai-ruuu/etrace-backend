from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base
from app.utils.datetime import get_utc_now

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    alumni: Mapped[list["AlumniProfile"]] = relationship("AlumniProfile", back_populates="course", uselist=False) # type: ignore
    is_inactive: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    is_archived: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    aligned_course_and_occupations: Mapped[list["AlignedCourseAndOccupation"]] = relationship("AlignedCourseAndOccupation", back_populates="course", uselist=True, cascade="all, delete-orphan") # type: ignore
    graduate_records: Mapped[list["GraduateRecord"]] = relationship("GraduateRecord", back_populates="course", uselist=True, cascade="all, delete-orphan") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

