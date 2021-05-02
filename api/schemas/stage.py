from typing import Dict, List

from pydantic import BaseModel

from api.schemas.pool import Pool


class StageBase(BaseModel):
    type: int
    params: Dict


class StageCreate(StageBase):
    pass


class Stage(StageBase):
    id: int
    tournament_id: int
    ordinal: int
    status: int
    pools: List[Pool]

    class Config:
        orm_mode = True
