from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.database import Base
from app.utils.datetime import get_utc_now

class Like(Base):
    __tablename__ = "likes"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    job_post_id: Mapped[int] = Column(Integer, ForeignKey("job_posts.id"))
    job_post: Mapped["JobPost"] = relationship("JobPost", back_populates="likes", uselist=False) # type: ignore
    alumni_profile_id: Mapped[int] = Column(Integer, ForeignKey("alumni_profiles.id"))
    alumni: Mapped["AlumniProfile"] = relationship("AlumniProfile", back_populates="likes", uselist=False) # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)
