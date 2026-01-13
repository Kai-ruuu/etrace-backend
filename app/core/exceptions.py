from fastapi import HTTPException, status

ACCOUNT_ALREADY_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account already exists.")

ACCOUNT_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Account not found.")

ACCOUNT_ALREADY_DISABLED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account is already disabled.")

ACCOUNT_ALREADY_ENABLED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account is already enabled.")

ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account should not be modified.")

ACCOUNT_CURRENTLY_DISABLED_EXCEPTION = HTTPException(status.HTTP_403_FORBIDDEN, "Account is currently disabled.")

UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to register account.")

ADMIN_ACCOUNT_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account already exists.")

AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email address or password.",
    headers={"WWW-Authenticate": "Bearer"}
)

PROFILE_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Profile not found.")

COMPANY_ALREADY_APPROVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Company is already approved.")

COMPANY_ALREADY_PENDING_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Company is already pending for approval.")

COMPANY_ALREADY_REJECTED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Company is already rejected.")

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

COURSE_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Course not found.")

COURSE_ALREADY_ARCHIVED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Course is already archived.")

COURSE_ALREADY_RESTORED_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Course is already restored.")

UNABLE_TO_CREATE_COURSE_EXCEPTION = HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create course.")

def FILE_TYPE_NOT_SUPPORTED_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"Unsopported file for {file_field.replace('_', ' ').capitalize()}."
    )

def IMAGE_FILE_CANNOT_BE_READ_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"Cannot read {file_field} image."
    )

def FILE_NOT_PROVIDED_EXCEPTION(file_field: str) -> None:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"{file_field.replace('_', ' ').capitalize()} is required."
    )

def FILE_NAME_LENGTH_TOO_LONG_EXCEPTION(file_field: str, name_length_limit: int) -> None:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"File name for {file_field.replace('_', ' ').capitalize()} is too long. It should not exceed {name_length_limit} characters."
    )

def FILE_SIZE_TOO_BIG_EXCEPTION(file_field: str, file_size_limit: int) -> None:
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"File size for {file_field.replace('_', ' ').capitalize()} is too big. It should not exceed {file_size_limit} Mb."
    )

