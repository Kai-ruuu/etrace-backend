from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum

from app.database import Base
from app.utils.datetime import get_utc_now
from app.enums.all import CompanyApprovalStatus

class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    logo_filename: Mapped[str] = Column(String(255), nullable=False)
    sec_filename: Mapped[str] = Column(String(255), nullable=False)
    profile_filename: Mapped[str] = Column(String(255), nullable=False)
    business_permit_filename: Mapped[str] = Column(String(255), nullable=False)
    list_of_vacancies_filename: Mapped[str] = Column(String(255), nullable=False)
    cert_from_dole_filename: Mapped[str] = Column(String(255), nullable=False)
    cert_of_no_pending_case_filename: Mapped[str] = Column(String(255), nullable=False)
    reg_dti_cda_filename: Mapped[str] = Column(String(255), nullable=False)
    reg_of_est_filename: Mapped[str] = Column(String(255), nullable=False)
    reg_philjobnet_filename: Mapped[str] = Column(String(255), nullable=False)
    account_id: Mapped[int] = Column(Integer, ForeignKey("accounts.id"), unique=True)
    account: Mapped["Account"] = relationship("Account", back_populates="company_profile") # type: ignore
    sysad_approval_status: Mapped[CompanyApprovalStatus] = Column(Enum(CompanyApprovalStatus), nullable=False, default=CompanyApprovalStatus.PENDING)
    peso_staff_approval_status: Mapped[CompanyApprovalStatus] = Column(Enum(CompanyApprovalStatus), nullable=False, default=CompanyApprovalStatus.PENDING)
    job_posts: Mapped[list["JobPost"]] = relationship("JobPost", back_populates="company", uselist=True, cascade="all, delete-orphan") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

