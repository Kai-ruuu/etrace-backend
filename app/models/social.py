from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime

from app.database import Base
from app.utils.datetime import get_utc_now

class Social(Base):
    __tablename__ = "socials"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    platform: Mapped[str] = Column(String(35), nullable=False)
    url: Mapped[str] = Column(Text, nullable=False)
    alumni_profile_id: Mapped[int] = Column(Integer, ForeignKey("alumni_profiles.id"))
    alumni: Mapped["AlumniProfile"] = relationship("AlumniProfile", back_populates="socials") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)
