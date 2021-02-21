from datetime import datetime
from typing import Optional, List

from pydantic.main import BaseModel

from api.schemas.security import User
from api.schemas.stage import Stage


class TournamentBase(BaseModel):
    name: str
    organization: Optional[str]
    start_date: datetime
    public: bool


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    pass


class TournamentBasic(TournamentBase):
    id: int
    status: int
    owner: User

    class Config:
        orm_mode = True


class TournamentDetail(TournamentBasic):
    stages: List[Stage]


class TournamentList(BaseModel):
    total: int
    items: List[TournamentBasic]
