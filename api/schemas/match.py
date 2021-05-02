from typing import Optional

from pydantic import BaseModel

from api.schemas.competitor import Competitor


class Match(BaseModel):
    id: int
    ordinal: int
    competitor_1: Optional[Competitor]
    competitor_1_score: Optional[int]
    competitor_2: Optional[Competitor]
    competitor_2_score: Optional[int]
    next_match_id: Optional[int]
    status: int

    class Config:
        orm_mode = True
