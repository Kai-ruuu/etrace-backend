from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum

from app.database import Base
from app.utils.datetime import get_utc_now
from app.enums.all import AlumniApprovalStatus, AlumniEmploymentStatus

class AlumniProfile(Base):
    __tablename__ = "alumni_profiles"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    profile_picture_filename: Mapped[str] = Column(String(255), nullable=False)
    curriculum_vitae_filename: Mapped[str | None] = Column(String(255), nullable=True, default=None)
    dean_approval_status: Mapped[AlumniApprovalStatus] = Column(Enum(AlumniApprovalStatus), nullable=False, default=AlumniApprovalStatus.PENDING)
    employment_status: Mapped[AlumniEmploymentStatus] = Column(Enum(AlumniEmploymentStatus), nullable=False, default=AlumniEmploymentStatus.UNEMPLOYED)
    prefix: Mapped[str | None] = Column(String(255), nullable=True)
    first_name: Mapped[str] = Column(String(255), nullable=False)
    middle_name: Mapped[str | None] = Column(String(255), nullable=True, default=None)
    last_name: Mapped[str] = Column(String(255), nullable=False)
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="alumni", uselist=True, cascade="all, delete-orphan") # type: ignore
    year_graduated: Mapped[int] = Column(Integer, nullable=False)
    occupation_states: Mapped[list["OccupationState"]] = relationship("OccupationState", back_populates="alumni", uselist=True, cascade="all, delete-orphan") # type: ignore
    address: Mapped[str] = Column(String(515), nullable=False)
    phone_number: Mapped[str] = Column(String(15), nullable=False)
    socials: Mapped[list["Social"]] = relationship("Social", back_populates="alumni", uselist=True, cascade="all, delete-orphan") # type: ignore
    course_id: Mapped[int] = Column(Integer, ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship("Course", back_populates="alumni") # type: ignore
    account_id: Mapped[int] = Column(Integer, ForeignKey("accounts.id"), unique=True)
    account: Mapped["Account"] = relationship("Account", back_populates="alumni_profile") # type: ignore
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False, default=get_utc_now, onupdate=get_utc_now)
