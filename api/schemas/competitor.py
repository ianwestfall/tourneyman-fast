from typing import Optional

from pydantic import BaseModel


class CompetitorBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    organization: Optional[str]
    location: Optional[str]


class CompetitorCreate(CompetitorBase):
    pass


class CompetitorUpdate(CompetitorBase):
    pass


class Competitor(CompetitorBase):
    id: int
    tournament_id: int

    class Config:
        orm_mode = True
