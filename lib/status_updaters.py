from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from database.models import Tournament


class TournamentStatusUpdater(ABC):
    """
    Used to update the status of a Tournament and perform any necessary database changes.
    Any db changes should not be committed.
    """

    def update(self, tournament: Tournament, status_change: int, db: Session):
        """
        Update the given tournament in the given direction.
        :param tournament:
        :param status_change: either 1 or -1 indicating the direction to change the status
        :param db:
        """
        if status_change == 1:
            self.up(tournament, db)
        elif status_change == -1:
            self.down(tournament, db)
        else:
            raise ValueError(f'Invalid value for status_change: {status_change}')

    @abstractmethod
    def up(self, tournament: Tournament, db: Session):
        raise NotImplementedError()

    @abstractmethod
    def down(self, tournament: Tournament, db: Session):
        raise NotImplementedError()

    @classmethod
    def update_status(cls, tournament: Tournament, status: int, db: Session):
        status_change = status - tournament.status
        if abs(status_change) > 1:
            # Can only move up or down by one status at a time.
            raise ValueError('Can only move up or down by one status at a time')
        elif status_change == 0:
            # No-op
            return
        else:
            updater = cls.get_status_updater(status)
            updater.update(tournament, status_change, db)

    @classmethod
    def get_status_updater(cls, status: int):
        updaters = {
            0: TournamentPendingStatusUpdater,
            1: TournamentReadyStatusUpdater,
            2: TournamentActiveStatusUpdater,
            3: TournamentCompleteStatusUpdater,
        }
        return updaters[status]()


class TournamentPendingStatusUpdater(TournamentStatusUpdater):
    """
    Handles changes to the Pending status
    """
    def up(self, tournament: Tournament, db: Session):
        raise NotImplementedError('Not possible to move up to pending status')

    def down(self, tournament: Tournament, db: Session):
        raise NotImplementedError('Not possible to move down to pending status')


class TournamentReadyStatusUpdater(TournamentStatusUpdater):
    """
    Handles changes to the Ready status
    """
    def up(self, tournament: Tournament, db: Session):
        """
        All that needs to be done is update the tournament's status
        """
        tournament.status += 1
        db.add(tournament)

    def down(self, tournament: Tournament, db: Session):
        """
        Any existing matches need to be deleted and all stages need to be reset.
        """
        raise NotImplementedError()


class TournamentActiveStatusUpdater(TournamentStatusUpdater):
    """
    Handles changes to the Active status
    """
    def up(self, tournament: Tournament, db: Session):
        """
        The first stage should be initialized
        """
        raise NotImplementedError()

    def down(self, tournament: Tournament, db: Session):
        """
        Not sure what this would do, other than allow stages to be undone?
        """
        raise NotImplementedError()


class TournamentCompleteStatusUpdater(TournamentStatusUpdater):
    """
    Handles changes to the Complete status
    """
    def up(self, tournament: Tournament, db: Session):
        """
        Finalize the tournament results
        """
        raise NotImplementedError()

    def down(self, tournament: Tournament, db: Session):
        raise NotImplementedError('Not possible to move down to complete status')
