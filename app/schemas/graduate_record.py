from datetime import datetime
from pydantic import BaseModel


class GraduateRecordOut(BaseModel):
    id: int
    record_filename: str
    is_archived: bool
    graduation_year: int
    course_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}