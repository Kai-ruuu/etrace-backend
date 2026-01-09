from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum

from app.enums.all import AccountRole
from app.database import Base
from app.utils.env import envs
from app.utils.datetime import get_utc_now

DEFAULT_SYSAD_EMAIL = envs("DEFAULT_SYSAD_EMAIL")

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
    def profile(self):
        role_profile_map = {
            AccountRole.SYSTEM_ADMINISTRATOR: self.system_admin_profile,
            AccountRole.DEAN: self.dean_profile,
            AccountRole.PESO_STAFF: self.peso_staff_profile,
            AccountRole.COMPANY: self.company_profile,
            AccountRole.ALUMNI: self.alumni_profile,
        }
        return role_profile_map.get(self.role, None)
    
    @property
    def is_default_system_admin(self) -> bool:
        return DEFAULT_SYSAD_EMAIL == self.email



    # creating accounts
    @property
    def can_create_system_admins(self) -> bool:
        return DEFAULT_SYSAD_EMAIL == self.email
    
    @property
    def can_create_deans(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR

    @property
    def can_create_peso_staffs(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR
    
    
    
    # reading accounts
    @property
    def can_read_system_admins(self) -> bool:
        return DEFAULT_SYSAD_EMAIL == self.email
    
    @property
    def can_read_deans(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR

    @property
    def can_read_peso_staffs(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR
    
    @property
    def can_read_companies(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR

    @property
    def can_read_alumni(self) -> bool:
        return self.role in {AccountRole.DEAN, AccountRole.SYSTEM_ADMINISTRATOR, AccountRole.COMPANY}



    # enabling and disabling accounts
    @property
    def can_enable_or_disable_system_admins(self) -> bool:
        return DEFAULT_SYSAD_EMAIL == self.email
    
    @property
    def can_enable_or_disable_deans(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR
    
    @property
    def can_enable_or_disable_peso_staffs(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR
    
    @property
    def can_enable_or_disable_companies(self) -> bool:
        return self.role in {AccountRole.SYSTEM_ADMINISTRATOR, AccountRole.PESO_STAFF}
    
    @property
    def can_enable_or_disable_alumni(self) -> bool:
        return self.role == AccountRole.DEAN
    
    
    # approving and rejecting accounts
    @property
    def can_approve_or_reject_alumni(self) -> bool:
        return self.role == AccountRole.DEAN
    
    @property
    def can_approve_or_reject_companies(self) -> bool:
        return self.role == AccountRole.PESO_STAFF



    # managing passwords
    @property
    def can_update_password(self) -> bool:
        return DEFAULT_SYSAD_EMAIL != self.email

    @property
    def can_forgot_password(self) -> bool:
        return DEFAULT_SYSAD_EMAIL != self.email

    # managing schools
    @property
    def can_manage_schools(self) -> bool:
        return self.role == AccountRole.SYSTEM_ADMINISTRATOR
    
    # managing courses
    @property
    def can_manage_courses(self) -> bool:
        return self.role == AccountRole.DEAN
    
    # managing graduate records
    @property
    def can_manage_graduate_records(self) -> bool:
        return self.role == AccountRole.DEAN
    
    # managing aligned courses and occupation
    @property
    def can_manage_aligned_courses_and_occupations(self) -> bool:
        return self.role == AccountRole.DEAN
    
    # managing job posts
    @property
    def can_manage_job_posts(self) -> bool:
        return self.role == AccountRole.COMPANY

