from fastapi import HTTPException, status

ACCOUNT_CURRENTLY_DISABLED_EXCEPTION = HTTPException(status.HTTP_403_FORBIDDEN, "Account is currently disabled.")

ADMIN_ACCOUNT_EXISTS_EXCEPTION = HTTPException(status.HTTP_409_CONFLICT, "Account already exists.")

AUTHENTICATION_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email address or password.",
    headers={"WWW-Authenticate": "Bearer"}
)

PROFILE_NOT_FOUND_EXCEPTION = HTTPException(status.HTTP_404_NOT_FOUND, "Profile not found.")

TOKEN_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED_ACCESS_EXCEPION = HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not authorized to access this resource.")

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

