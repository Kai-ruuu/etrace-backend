from datetime import datetime
from pydantic import BaseModel


class OccupationIn(BaseModel):
    title: str


class OccupationOut(BaseModel):
    id: int
    title: str
    normalized_title: str
    model_config = {"from_attributes": True}


class OccupationDeanListOut(OccupationOut):
    @classmethod
    def model_validate_custom(cls, row) -> dict:
        occupation, is_aligned = row
        data = cls.model_validate(occupation).model_dump()
        data["is_aligned"] = is_aligned
        return data