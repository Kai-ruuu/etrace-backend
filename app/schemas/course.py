from datetime import datetime
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    name: str = Field(..., min_length=4, max_length=255)


class CourseIn(CourseBase):
    pass


class CourseOut(BaseModel):
    name: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

