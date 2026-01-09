from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base
from app.utils.datetime import get_utc_now

class School(Base):
    __tablename__ = "schools"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    assigned_deans: Mapped[list["DeanProfile"]] = relationship("DeanProfile", back_populates="school", uselist=False) # type: ignore
    is_archived: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

