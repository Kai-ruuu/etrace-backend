from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum

from app.database import Base
from app.utils.datetime import get_utc_now
from app.enums.all import JobPostWorkSetup, JobPostEmploymentType

class JobPost(Base):
    __tablename__ = "job_posts"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    requirements: Mapped[str] = Column(Text, nullable=False)
    responsibilities: Mapped[str] = Column(Text, nullable=False)
    location: Mapped[str] = Column(String(1025), nullable=False)
    application_steps: Mapped[str] = Column(Text, nullable=False)
    work_setup: Mapped[JobPostWorkSetup] = Column(Enum(JobPostWorkSetup), nullable=False, default=JobPostWorkSetup.ON_SITTE)
    employment_type: Mapped[JobPostEmploymentType] = Column(Enum(JobPostEmploymentType), nullable=False, default=JobPostEmploymentType.FULL_TIME)
    salary_min: Mapped[int] = Column(Integer, nullable=False)
    salary_max: Mapped[int] = Column(Integer, nullable=False)
    is_archived: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    is_posted_already: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    is_payment_monthly: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    company_profile_id: Mapped[int] = Column(Integer, ForeignKey("company_profiles.id"), nullable=False)
    company: Mapped["CompanyProfile"] = relationship("CompanyProfile", back_populates="job_posts") # type: ignore
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="job_post") # type: ignore
    posted_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)

