from datetime import datetime
from pydantic import BaseModel, Field

class SchoolBase(BaseModel):
    id: int
    name: str = Field(..., min_length=9, max_length=65)
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class SchoolIn(BaseModel):
    name: str = Field(..., min_length=9, max_length=65)

class SchoolOut(SchoolBase):
    model_config = {"from_attributes": True}

class SchoolUpdate(SchoolIn):
    pass