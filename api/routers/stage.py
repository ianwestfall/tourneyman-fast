from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api.routers.tournament import alterable_tournament, visible_tournament
from api.schemas.stage import StageCreate, Stage as StageSchema
from database.db import get_db
from database.models import Stage, Tournament

# All routes will receive a tournament_id path parameter
router = APIRouter(prefix='/tournaments/{tournament_id}/stages', tags=['stage'])


async def get_stage_by_id(stage_id: int, db: Session = Depends(get_db)) -> Optional[Stage]:
    return Stage.by_id(stage_id, db)


@router.post('/', response_model=List[StageSchema], status_code=status.HTTP_201_CREATED)
async def create_stage(
        tournament_id: int,
        stages: List[StageCreate],
        tournament: Tournament = Depends(alterable_tournament),
        db: Session = Depends(get_db),
):
    """
    Creates new stages owned by the given tournament_id if the current_user owns it and the stages are valid to be
    appended to the tournament's existing stages, if any.
    """
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No tournament found with id {tournament_id}',
        )
    try:
        return [Stage.create(tournament, stage, db) for stage in stages]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


# noinspection PyTypeChecker
@router.get('/', response_model=List[StageSchema])
async def get_stages(
        tournament_id: int,
        tournament: Tournament = Depends(visible_tournament),
):
    """
    Gets all stages for the given tournament, if it exists and is visible to the current user
    """
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No tournament found with id {tournament_id}',
        )
    else:
        return tournament.stages


@router.get('/{stage_id}', response_model=StageSchema)
async def get_stage(
        tournament_id: int,
        stage_id: int,
        tournament: Tournament = Depends(visible_tournament),
        stage: Stage = Depends(get_stage_by_id),
):
    """
    Gets the stage with the given ID, if it exists within the given tournament and is visible to the current user
    """
    if not tournament or not stage or stage.tournament != tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No stage found with id {stage_id} for tournament {tournament_id}',
        )
    else:
        return stage


@router.delete('/{stage_id}')
async def delete_stage(
        tournament_id: int,
        stage_id: int,
        tournament: Tournament = Depends(alterable_tournament),
        stage: Stage = Depends(get_stage_by_id),
        db: Session = Depends(get_db),
):
    """
    Deletes the stage with the given ID, if it exists within the given tournament and is editable by the current user
    and is currently the final stage in the tournament
    """
    if not tournament or not stage or stage.tournament != tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No stage found with id {stage_id} for tournament {tournament_id}',
        )
    else:
        try:
            stage.delete(db)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )
