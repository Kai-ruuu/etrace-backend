from datetime import datetime
from pydantic import BaseModel

class CourseBase(BaseModel):
    id: int
    name: str
    is_inactive: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime

