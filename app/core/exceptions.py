from fastapi import HTTPException, status

ACCOUNT_ALREADY_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account already exists.")


ACCOUNT_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Account not found.")

ACCOUNT_ALREADY_DISABLED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account is already disabled.")

ACCOUNT_ALREADY_ENABLED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account is already enabled.")

ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account should not be modified.")

ACCOUNT_CURRENTLY_DISABLED_EXCEPTION = HTTPException(status.HTTP_403_FORBIDDEN, "Account is currently disabled.")

UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to register account.")

AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email address or password.",
    headers={"WWW-Authenticate": "Bearer"}
)

def RAISE_INVALID_EMAIL_EXCEPTION(error_message: str = "Invalid email format."):
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, error_message)
    
EMAIL_INVALID_EXCEPTION = HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Invalid email format.")

PROFILE_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Profile not found.")

COMPANY_ALREADY_APPROVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Company is already approved.")

COMPANY_ALREADY_PENDING_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Company is already pending for approval.")

COMPANY_ALREADY_REJECTED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Company is already rejected.")

COMPANY_PROFILE_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Company profile not found.")

ALUMNI_ALREADY_APPROVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Alumni is already approved.")

ALUMNI_ALREADY_PENDING_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Alumni is already pending for approval.")

ALUMNI_ALREADY_REJECTED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Alumni is already rejected.")

TOKEN_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED_ACCESS_EXCEPION = HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not authorized to access this resource.")

SCHOOLS_EMPTY_EXCEPTION = HTTPException(status.HTTP_403_FORBIDDEN, "Please create at least one school first.")

SCHOOL_ALREADY_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "School already exists.")

SCHOOL_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "School not found.")

SCHOOL_ALREADY_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "School is already archived.")

SCHOOL_ALREADY_RESTORED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "School is already restored.")

SCHOOL_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "School not found.")

UNABLE_TO_CREATE_SCHOOL_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create school.")

COURSE_ALREADY_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Course already exists.")

def RAISE_COURSES_NOT_FOUND_BY_IDS(ids: list[int]) -> None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Course with ids ({', '.join(ids)}) were not found.")

COURSE_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Course not found.")

COURSE_ALREADY_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Course is already archived.")

COURSE_ALREADY_RESTORED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Course is already restored.")

UNABLE_TO_CREATE_COURSE_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create course.")

GRADUATE_RECORD_ALREADY_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Graduate record already exists.")

GRADUATE_RECORD_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Graduate record not found.")

GRADUATE_RECORD_ALREADY_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Graduate record is already archived.")

GRADUATE_RECORD_ALREADY_RESTORED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Graduate record is already restored.")

UNABLE_TO_CREATE_GRADUATE_RECORD_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create graduate record.")

JOB_POST_ALREADY_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post already exists.")

JOB_POST_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Job post not found.")

JOB_POST_ALREADY_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is already archived.")

JOB_POST_ALREADY_RESTORED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is already restored.")

JOB_POST_ALREADY_UNPUBLISHED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is already not published.")

JOB_POST_ALREADY_PUBLISHED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is already published.")

JOB_POST_PUBLISH_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is currently archived. Please restore it fist before publishing.")

JOB_POST_UNPUBLISH_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is currently archived. Please restore it fist before unpublishing.")

JOB_POST_ARCHIVE_PUBLISHED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Job post is currently published. Please unpublish it first before archiving.")

UNABLE_TO_CREATE_JOB_POST_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create job post.")

def RAISE_FILE_CANNOT_BE_READ_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"Cannot read {file_field}."
    )

def FILE_TYPE_NOT_SUPPORTED_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"Unsopported file for {file_field.replace('_', ' ').capitalize()}."
    )

def IMAGE_FILE_CANNOT_BE_READ_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"Cannot read {file_field} image."
    )

def FILE_NOT_PROVIDED_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"{file_field.replace('_', ' ').capitalize()} is required."
    )

def FILE_NAME_LENGTH_TOO_LONG_EXCEPTION(file_field: str, name_length_limit: int) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"File name for {file_field.replace('_', ' ').capitalize()} is too long. It should not exceed {name_length_limit} characters."
    )

def FILE_SIZE_TOO_BIG_EXCEPTION(file_field: str, file_size_limit: int) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"File size for {file_field.replace('_', ' ').capitalize()} is too big. It should not exceed {file_size_limit} Mb."
    )

def RAISE_CSV_MISSING_COLUMNS_EXCEPTION(missing_columns: set[str]) -> None:
    missing_columns = ", ".join(missing_columns)
    
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"Unable to process the record, please add these missing columns and their data: {missing_columns}"
    )

def RAISE_CSV_MISSING_COLUMN_VALUE_EXCEPTION(column: str) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f"There are rows where the required \"{column}\" column has no value."
    )

def RAISE_CSV_INCONSISTENT_DATE_FORMAT_EXCEPTION(column: str) -> None:
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        f'There are rows where the date column "{column}" has a different format from the others.'
    )