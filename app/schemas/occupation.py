from datetime import datetime
from pydantic import BaseModel


class OccupationIn(BaseModel):
    title: str