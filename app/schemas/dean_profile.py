from datetime import datetime
from pydantic import BaseModel

class DeanProfileBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    model_config = {"from_attributes": True}

class DeanProfileOut(DeanProfileBase):
    id: int
    account_id: int
    school_id: int
    # school: SchoolOut
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}