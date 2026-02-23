from enum import StrEnum, auto

class Action(StrEnum):
    CREATE_SYSTEM_ADMINS = auto()
    READ_SYSTEM_ADMINS = auto()
    ENABLE_DISABLE_SYSTEM_ADMINS = auto()
    CREATE_DEANS = auto()
    READ_DEANS = auto()
    ENABLE_DISABLE_DEANS = auto()
    APPROVE_COMPANIES = auto()
    REJECT_COMPANIES = auto()
    PEND_COMPANIES = auto()
    READ_COMPANIES = auto()
    ENABLE_DISABLE_COMPANIES = auto()
    CREATE_PESO_STAFFS = auto()
    READ_PESO_STAFFS = auto()
    ENABLE_DISABLE_PESO_STAFFS = auto()
    CREATE_SCHOOLS = auto()
    READ_SCHOOLS = auto()
    ARCHIVE_RESTORE_SCHOOLS = auto()
    CREATE_COURSES = auto()
    READ_COURSES = auto()
    ARCHIVE_RESTORE_COURSES = auto()
    READ_ALUMNI = auto()
    ENABLE_DISABLE_ALUMNI = auto()
    APPROVE_ALUMNI = auto()
    REJECT_ALUMNI = auto()
    PEND_ALUMNI = auto()
    CREATE_GRADUATE_RECORDS = auto()
    READ_GRADUATE_RECORDS = auto()
    ARCHIVE_RESTORE_GRADUATE_RECORDS = auto()
    CREATE_JOB_POSTS = auto()
    READ_JOB_POSTS = auto()
    INTERACT_WITH_JOB_POSTS = auto()
    ARCHIVE_RESTORE_JOB_POSTS = auto()
    PUBLISH_UNPUBLISH_JOB_POSTS = auto()
    READ_JOB_POST_INTERESTS = auto()
    REVIEW_UNREVIEW_JOB_POST_INTERESTS = auto()
    GET_ALUMNI_LOCATION_INFO = auto()
    UPDATE_DEAN_SCHOOL = auto()
    READ_OCCUPATIONS = auto()
    CREATE_OCCUPATIONS = auto()
    ALIGN_UNALIGN_OCCUPATIONS = auto()


class AccountRole(StrEnum):
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    DEAN = "DEAN"
    PESO_STAFF = "PESO_STAFF"
    COMPANY = "COMPANY"
    ALUMNI = "ALUMNI"

    @classmethod
    def is_valid(_class, role: str) -> bool:
        return role in _class._value2member_map_
    
    @classmethod
    def all(_class) -> list:
        return [_class.SYSTEM_ADMIN, _class.DEAN, _class.PESO_STAFF, _class.COMPANY, _class.ALUMNI]

    @classmethod
    def as_display(_class, role: str) -> str:
        if not _class.is_valid(role):
            return None
        
        role_display_map = {
            _class.SYSTEM_ADMIN: 'System Administrator',
            _class.PESO_STAFF: 'PESO Staff',
            _class.DEAN: 'Dean',
            _class.COMPANY: 'Company',
            _class.ALUMNI: 'Alumni',
        }
        
        return role_display_map[role]

class AlumniApprovalStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AlumniEmploymentStatus(StrEnum):
    EMPLOYED = "EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    SELF_EMPLOYED = "SELF_EMPLOYED"

class CompanyApprovalStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class JobPostWorkSetup(StrEnum):
    ON_SITTE = "ON_SITTE"
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"

class JobPostEmploymentType(StrEnum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"

