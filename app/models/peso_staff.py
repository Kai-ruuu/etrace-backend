from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base
from app.utils.datetime import get_utc_now

class PesoStaffProfile(Base):
    __tablename__ = "peso_staff_profiles"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = Column(String(255), nullable=False)
    middle_name: Mapped[str | None] = Column(String(255), nullable=True, default=None)
    last_name: Mapped[str] = Column(String(255), nullable=False)
    account_id: Mapped[int] = Column(Integer, ForeignKey("accounts.id"), unique=True)
    account: Mapped["Account"] = relationship("Account", back_populates="peso_staff_profile") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)
