from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=65)