from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

from app.database import Base
from app.utils.datetime import get_utc_now

class OccupationState(Base):
    __tablename__ = "occupation_states"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    location: Mapped[str] = Column(String(1025), nullable=False)
    is_current: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    occupation_id: Mapped[int] = Column(Integer, ForeignKey("occupations.id"))
    occupation: Mapped["Occupation"] = relationship("Occupation", back_populates="occupation_states") # type: ignore
    alumni_id: Mapped[int] = Column(Integer, ForeignKey("alumni_profiles.id"))
    alumni: Mapped["AlumniProfile"] = relationship("AlumniProfile", back_populates="occupation_states") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

