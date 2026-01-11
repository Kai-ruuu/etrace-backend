from datetime import datetime
from pydantic import BaseModel

class PesoStaffProfileBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    model_config = {"from_attributes": True}

class PesoStaffProfileOut(PesoStaffProfileBase):
    id: int
    account_id: int
    account_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}