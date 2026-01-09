from datetime import datetime
from pydantic import BaseModel

from app.schemas.school import SchoolBase

class DeanProfileBase(BaseModel):
    id: int
    school_id: int
    account_id: int
    first_name: str
    middle_name: str | None
    last_name: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class DeanAdminProfileOut(DeanProfileBase):
    school: SchoolBase
    model_config = {"from_attributes": True}

