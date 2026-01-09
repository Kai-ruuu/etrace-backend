from datetime import datetime
from pydantic import BaseModel

class PesoStaffProfileBase(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str
    account_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class PesoStaffProfileOut(PesoStaffProfileBase):
    model_config = {"from_attributes": True}

