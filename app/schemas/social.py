from json import loads
from datetime import datetime
from pydantic import BaseModel, Field

class Social(BaseModel):
    platform: str = Field(..., min_length=1, max_length=35)
    url: str = Field(..., min_length=1)
