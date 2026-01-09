from enum import Enum

class JobPostWorkSetup(str, Enum):
    ON_SITTE = "ON_SITTE"
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"

class JobPostEmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"

