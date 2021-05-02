from typing import List

from pydantic.main import BaseModel

from api.schemas.match import Match


class Pool(BaseModel):
    id: int
    ordinal: int
    matches: List[Match]

    class Config:
        orm_mode = True
