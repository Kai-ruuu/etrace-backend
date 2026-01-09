from datetime import datetime
from pydantic import BaseModel

class SystemAdminProfileBase(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str
    account_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class SystemAdminProfileOut(SystemAdminProfileBase):
    model_config = {"from_attributes": True}

