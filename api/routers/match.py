from typing import List

from fastapi import APIRouter, Depends

from api.routers.tournament import visible_tournament
from database.models import Tournament

router = APIRouter(prefix='/tournaments/{tournament_id}/stages/{stage_id}}/matches', tags=['match'])


@router.get('/', response_model=List[MatchSchema])
async def get_matches(
        tournament_id: int,
        stage_id: int,
        tournament: Tournament = Depends(visible_tournament)):
    pass
