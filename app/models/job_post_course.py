from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.core.database import Base
from app.utils.datetime import get_utc_now

class JobPostCourse(Base):
    __tablename__ = "job_post_course"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    job_post_id: Mapped[int] = Column(Integer, ForeignKey("job_posts.id"))
    job_post: Mapped["JobPost"] = relationship("JobPost", back_populates="job_post_courses", uselist=False) # type: ignore
    job_post_course_id: Mapped[int] = Column(Integer, ForeignKey("courses.id"))
    job_post_course: Mapped["Course"] = relationship("Course", back_populates="course_job_posts", uselist=False) # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)
