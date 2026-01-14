from datetime import datetime
from pydantic import BaseModel


class OccupationStateIn(BaseModel):
    location: str
    is_current: bool