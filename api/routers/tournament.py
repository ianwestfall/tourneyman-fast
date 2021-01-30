from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api.routers.security import get_current_active_user, get_current_active_user_or_none
from api.schemas.tournament import Tournament as TournamentSchema, TournamentCreate, TournamentUpdate, TournamentList
from database.db import get_db
from database.models import User, Tournament

router = APIRouter()


@router.post('/', response_model=TournamentSchema, status_code=status.HTTP_201_CREATED)
async def create_tournament(
        tournament: TournamentCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    """
    Creates a new tournament owned by the current user
    """
    return Tournament.create(tournament, current_user, db)


# noinspection PyTypeChecker
@router.get('/', response_model=TournamentList)
async def get_tournaments(
        is_filtered_by_user: bool = False, skip: int = 0, limit: int = 100,
        current_user: Optional[User] = Depends(get_current_active_user_or_none),
        db: Session = Depends(get_db),
):
    """
    Return all public tournaments and any private tournaments owned by the current_user, if present
    """
    tournament_count = len(Tournament.get_all_visible(current_user, db, is_filtered_by_user))
    tournaments = Tournament.get_all_visible(current_user, db, is_filtered_by_user, skip, limit)
    return {
        'total': tournament_count,
        'items': tournaments,
    }


@router.get('/{tournament_id}', response_model=TournamentSchema)
async def get_tournament(
        tournament_id: int,
        current_user: Optional[User] = Depends(get_current_active_user_or_none),
        db: Session = Depends(get_db),
):
    """
    Gets the tournament with the given ID, if it exists and is visible to the current user
    """
    tournament = Tournament.by_id_visible(tournament_id, current_user, db)
    if tournament:
        return tournament
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No tournament found with id {tournament_id}',
        )


@router.put('/{tournament_id}', response_model=TournamentSchema)
async def update_tournament(
        tournament_id: int,
        tournament: TournamentUpdate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    """
    Updates the desired tournament if the current user owns it
    """
    db_tournament = Tournament.by_id_visible(tournament_id, current_user, db)
    if db_tournament and db_tournament.owner == current_user:
        db_tournament.update(tournament, db)
        return db_tournament
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No editable tournament found with id {tournament_id} for user {current_user.email}',
        )


@router.delete('/{tournament_id}')
async def delete_tournament(
        tournament_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    """
    Deletes the desired tournament if the current user owns it
    """
    db_tournament = Tournament.by_id_visible(tournament_id, current_user, db)
    if db_tournament and db_tournament.owner == current_user:
        db_tournament.delete(db)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No editable tournament found with id {tournament_id} for user {current_user.email}',
        )
