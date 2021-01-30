from datetime import datetime
from typing import Optional, List

from pydantic.main import BaseModel

from api.schemas.security import User


class TournamentBase(BaseModel):
    name: str
    organization: Optional[str]
    start_date: datetime
    public: bool


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: int
    status: int
    owner: User

    class Config:
        orm_mode = True


class TournamentList(BaseModel):
    total: int
    items: List[Tournament]
