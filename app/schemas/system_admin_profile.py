from datetime import datetime
from pydantic import BaseModel, Field


class SystemAdminProfileBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str


# [mark] ensure string length range was properly set
class SystemAdminProfileIn(SystemAdminProfileBase):
    pass


class SystemAdminProfileOut(SystemAdminProfileBase):
    id: int
    account_id: int
    account_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


