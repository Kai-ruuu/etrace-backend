from datetime import datetime
from pydantic import BaseModel


class DeanProfileBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    
    
class DeanProfileIn(DeanProfileBase):
    pass


class DeanProfileOut(DeanProfileBase):
    id: int
    account_id: int
    school_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}