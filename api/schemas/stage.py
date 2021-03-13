from typing import Dict

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
