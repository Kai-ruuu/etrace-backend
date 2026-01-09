from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.database import Base
from app.utils.datetime import get_utc_now

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    action: Mapped[str] = Column(String(255), nullable=False)
    account_id: Mapped[int] = Column(Integer, ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship("Account", back_populates="audit_logs") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)

