from datetime import datetime
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    name: str = Field(..., min_length=4, max_length=255)


class CourseIn(CourseBase):
    school_id: int


class CourseOut(BaseModel):
    id: int
    name: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

