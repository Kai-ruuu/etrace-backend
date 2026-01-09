from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from app.database import Base
from app.utils.datetime import get_utc_now

class GraduateRecord(Base):
    __tablename__ = "graduate_records"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    record_filename: Mapped[str] = Column(String(255), nullable=False, unique=True)
    is_archived: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    graduation_year: Mapped[int] = Column(Integer, nullable=False)
    course_id: Mapped[int] = Column(Integer, ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship("Course", back_populates="graduate_records") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

