from fastapi import HTTPException, status

ACCOUNT_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Account not found."
)

ACCOUNT_ALREADY_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Account already exists."
)

ACCOUNT_CURRENTLY_DISABLED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Account is currently disabled."
)

ACCOUNT_ALREADY_DISABLED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Account is already disabled."
)

ACCOUNT_ALREADY_ENABLED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Account is already enabled."
)

ACCOUNT_UNABLE_TO_CREATE_EXCEPTION = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Unable to create account."
)

PROFILE_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Profile not found."
)

SCHOOL_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="School not found."
)

SCHOOL_ALREADY_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="School already exists."
)

SCHOOL_ALREADY_ARCHIVED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="School is already archived."
)

SCHOOL_ALREADY_RESTORED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="School is already restored."
)

SCHOOL_ALREADY_INACTIVE_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="School is already inactive."
)

SCHOOL_ALREADY_ACTIVE_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="School is already active."
)

SCHOOLS_CURRENTLY_EMPTY_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="There are no schools yet, please create at least one first."
)

CHANGE_PASSWORD_INCORRECT_PASSWORD_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Password is not correct."
)

ROLE_INVALID_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid role."
)

AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email address or password.",
    headers={"WWW-Authenticate": "Bearer"}
)

TOKEN_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED_ACCESS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not authorized to access this resource."
)

def RAISE_FILE_TYPE_NOT_SUPPORTED_EXCEPTION_FOR(file_field: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsopported file for {file_field.replace('_', ' ').capitalize()}."
    )

def RAISE_IMAGE_FILE_CANNOT_BE_READ_EXCEPTION_FOR(file_field: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Cannot read {file_field} image."
    )

def RAISE_FILE_NOT_PROVIDED_EXCEPTION_FOR(file_field: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{file_field.replace('_', ' ').capitalize()} is required."
    )

def RAISE_FILE_NAME_LENGTH_TOO_LONG_EXCEPTION_FOR(file_field: str, name_length_limit: int) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"File name for {file_field.replace('_', ' ').capitalize()} is too long. It should not exceed {name_length_limit} characters."
    )

def RAISE_FILE_SIZE_TOO_BIG_EXCEPTION_FOR(file_field: str, file_size_limit: int) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"File size for {file_field.replace('_', ' ').capitalize()} is too big. It should not exceed {file_size_limit} Mb."
    )

