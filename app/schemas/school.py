from datetime import datetime
from pydantic import BaseModel, Field


class SchoolBase(BaseModel):
    name: str = Field(..., min_length=9, max_length=255)


class SchoolIn(SchoolBase):
    pass


class SchoolOut(BaseModel):
    id: int
    name: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

