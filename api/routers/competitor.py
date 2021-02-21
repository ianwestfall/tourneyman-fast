import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.routers.tournament import alterable_tournament, visible_tournament
from api.schemas.competitor import Competitor as CompetitorSchema, CompetitorCreate, CompetitorUpdate
from database.db import get_db
from database.models import Tournament, Competitor


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/tournaments/{tournament_id}/competitors', tags=['competitor'])


async def get_competitor_by_id(competitor_id: int, db: Session = Depends(get_db)) -> Optional[Competitor]:
    return Competitor.by_id(competitor_id, db)


@router.post('/', response_model=CompetitorSchema, status_code=status.HTTP_201_CREATED)
async def create_competitor(
        tournament_id: int,
        competitor: CompetitorCreate,
        tournament: Tournament = Depends(alterable_tournament),
        db: Session = Depends(get_db),
):
    """
    Creates a new competitor for the given tournament if the current user owns it
    """
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No tournament found with id {tournament_id}',
        )
    else:
        try:
            return Competitor.create(tournament, competitor, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Competitors must have at least a last name or an organization',
            )


# noinspection PyTypeChecker
@router.post('/batch', response_model=List[CompetitorSchema])
async def create_competitors(
        tournament_id: int,
        competitors: List[CompetitorCreate],
        tournament: Tournament = Depends(alterable_tournament),
        db: Session = Depends(get_db),
):
    """
    Creates multiple competitors for the given tournament if the current user owns it
    """
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No tournament found with id {tournament_id}',
        )
    else:
        try:
            return Competitor.create_batch(tournament, competitors, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Competitors must have at least a last name or an organization',
            )


# noinspection PyTypeChecker
@router.get('/', response_model=List[CompetitorSchema])
async def get_competitors(
        tournament_id: int,
        tournament: Tournament = Depends(visible_tournament),
):
    """
    Gets the competitors for the given tournament if it is visible to the current user
    """
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No tournament found with id {tournament_id}',
        )
    else:
        return tournament.competitors


@router.get('/{competitor_id}', response_model=CompetitorSchema)
async def get_competitor(
        tournament_id: int,
        competitor_id: int,
        tournament: Tournament = Depends(visible_tournament),
        competitor: Competitor = Depends(get_competitor_by_id),
):
    """
    Gets the competitor with the given ID if it exists within the given tournament
    """
    if not tournament or not competitor or competitor.tournament != tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No competitor found with id {competitor_id} for tournament {tournament_id}',
        )
    else:
        return competitor


@router.put('/{compoetitor_id}', response_model=CompetitorSchema)
async def update_competitor(
        tournament_id: int,
        competitor_id: int,
        competitor_data: CompetitorUpdate,
        tournament: Tournament = Depends(alterable_tournament),
        competitor: Competitor = Depends(get_competitor_by_id),
        db: Session = Depends(get_db),
):
    """
    Updates the competitor with the given data if it exists within the give tournament and is editable by the current
    user
    """
    if not tournament or not competitor or competitor.tournament != tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No competitor found with id {competitor_id} for tournament {tournament_id}',
        )
    else:
        competitor.update(competitor_data, db)
        return competitor


@router.delete('/{competitor_id}')
async def delete_competitor(
        tournament_id: int,
        competitor_id: int,
        tournament: Tournament = Depends(alterable_tournament),
        competitor: Competitor = Depends(get_competitor_by_id),
        db: Session = Depends(get_db),
):
    """
    Deletes the competitor with the given ID if it exists within the given tournament and is editable by the current
    user
    """
    if not tournament or not competitor or competitor.tournament != tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No competitor found with id {competitor_id} for tournament {tournament_id}',
        )
    else:
        competitor.delete(db)
