from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum

from app.core.database import Base
from app.core.enums import AccountRole
from app.utils.datetime import get_utc_now
from app.core.permissions import Permissions

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    role: Mapped[AccountRole] = Column(Enum(AccountRole), nullable=False, default=AccountRole.ALUMNI)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = Column(String(255), nullable=False)
    is_disabled: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    system_admin_profile: Mapped["SystemAdminProfile"] = relationship("SystemAdminProfile", back_populates="account", uselist=False, cascade="all, delete-orphan") # type: ignore
    dean_profile: Mapped["DeanProfile"] = relationship("DeanProfile", back_populates="account", uselist=False, cascade="all, delete-orphan") # type: ignore
    peso_staff_profile: Mapped["PesoStaffProfile"] = relationship("PesoStaffProfile", back_populates="account", uselist=False, cascade="all, delete-orphan") # type: ignore
    company_profile: Mapped["CompanyProfile"] = relationship("CompanyProfile", back_populates="account", uselist=False, cascade="all, delete-orphan") # type: ignore
    alumni_profile: Mapped["AlumniProfile"] = relationship("AlumniProfile", back_populates="account", uselist=False, cascade="all, delete-orphan") # type: ignore
    audit_logs: Mapped["AuditLog"] = relationship("AuditLog", back_populates="account", uselist=True, cascade="all, delete-orphan") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

    @property
    def permissions(self):
        return Permissions(self)