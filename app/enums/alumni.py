from enum import Enum

class AlumniApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AlumniEmploymentStatus(str, Enum):
    EMPLOYED = "EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    SELF_EMPLOYED = "SELF_EMPLOYED"

