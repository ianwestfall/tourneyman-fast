from typing import List

import pytest

from database.models import Tournament, Stage, Match, TournamentError
from tests.factories import TournamentFactory, StageFactory, CompetitorFactory
from tests.utils import DatabaseAwareTest


# noinspection PyMethodMayBeStatic
class TestTournament(DatabaseAwareTest):
    def test_delete_stages_no_stages_is_a_noop(self, db):
        tournament: Tournament = TournamentFactory()
        tournament.delete_stages(db)

        assert len(tournament.stages) == 0
        assert len(db.query(Stage).all()) == 0

    def test_delete_stages_all_are_removed(self, db):
        tournament: Tournament = TournamentFactory(stages=3)
        tournament.delete_stages(db)

        assert len(tournament.stages) == 0
        assert len(db.query(Stage).all()) == 0

    def test_delete_stages_no_commit_when_autocommit_is_false(self, db):
        tournament: Tournament = TournamentFactory(stages=3)
        existing_stage_ids = [stage.id for stage in tournament.stages]
        tournament.delete_stages(db, autocommit=False)

        db.refresh(tournament)
        assert len(tournament.stages) == 3
        assert [stage.id for stage in tournament.stages] == existing_stage_ids

    def test_delete_competitors_none_exist_noop(self, db):
        tournament: Tournament = TournamentFactory()
        tournament.delete_competitors(db)

        assert len(tournament.competitors) == 0

    def test_delete_competitors(self, db):
        tournament: Tournament = TournamentFactory(competitors=10)
        tournament.delete_competitors(db)

        assert len(tournament.competitors) == 0

    def test_delete_competitors_autocommit_is_false_no_changes(self, db):
        tournament: Tournament = TournamentFactory(competitors=10)
        tournament.delete_competitors(db, autocommit=False)

        assert len(tournament.competitors) == 10

    def test_progress_tournament_ready_starts_first_stage_and_sets_status_to_active(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2},
                                    tournament__status=Tournament.TournamentStatus.READY)
        tournament: Tournament = stage.tournament
        CompetitorFactory.create_batch(2, tournament=tournament)

        tournament.progress(db, autocommit=True)

        # Verify the first stage is active and has pools/matches
        assert stage.status == Stage.StageStatus.ACTIVE
        assert len(stage.pools) == 1
        assert len(stage.pools[0].matches) == 1

        # Verify the tournament is active
        assert tournament.status == Tournament.TournamentStatus.ACTIVE

    def test_progress_tournament_active_with_multiple_active_stages_raises_error(self, db):
        tournament: Tournament = TournamentFactory(status=Tournament.TournamentStatus.ACTIVE)
        stages: List[Stage] = [
            StageFactory(tournament=tournament, status=Stage.StageStatus.ACTIVE, ordinal=0),
            StageFactory(tournament=tournament, status=Stage.StageStatus.ACTIVE, ordinal=1),
            StageFactory(tournament=tournament, status=Stage.StageStatus.PENDING, ordinal=2),
        ]

        with pytest.raises(TournamentError):
            tournament.progress(db, autocommit=True)

        # Make sure the tournament status is unchanged
        assert tournament.status == Tournament.TournamentStatus.ACTIVE

        # Make sure the stage statuses are unchanged
        assert [stage.status for stage in stages] == [Stage.StageStatus.ACTIVE, Stage.StageStatus.ACTIVE,
                                                      Stage.StageStatus.PENDING]

    def test_progress_tournament_active_with_no_active_stages_raises_error(self, db):
        tournament: Tournament = TournamentFactory(status=Tournament.TournamentStatus.ACTIVE)
        stages: List[Stage] = [
            StageFactory(tournament=tournament, status=Stage.StageStatus.PENDING, ordinal=0),
            StageFactory(tournament=tournament, status=Stage.StageStatus.PENDING, ordinal=1),
            StageFactory(tournament=tournament, status=Stage.StageStatus.PENDING, ordinal=2),
        ]

        with pytest.raises(TournamentError):
            tournament.progress(db, autocommit=True)

        # Make sure the tournament status is unchanged
        assert tournament.status == Tournament.TournamentStatus.ACTIVE

        # Make sure the stage statuses are unchanged
        assert {stage.status for stage in stages} == {Stage.StageStatus.PENDING}

    def test_progress_tournament_active_progresses_the_active_stage_and_starts_the_next_one(self, db):
        tournament: Tournament = TournamentFactory(status=Tournament.TournamentStatus.ACTIVE)
        stages: List[Stage] = [
            StageFactory(
                tournament=tournament,
                status=Stage.StageStatus.PENDING,
                ordinal=idx,
                params={'minimum_pool_size': 2},
            )
            for idx in range(3)
        ]
        CompetitorFactory.create_batch(2, tournament=tournament)

        # Start the first stage and finish all of its matches
        stages[0].progress(db, autocommit=True)
        db.query(Match).filter(Match.pool == stages[0].pools[0]).update({Match.status: Match.MatchStatus.COMPLETE})

        tournament.progress(db, autocommit=True)

        # Verify that the tournament is still active
        assert tournament.status == Tournament.TournamentStatus.ACTIVE

        # Verify that the first stage is complete
        assert stages[0].status == Stage.StageStatus.COMPLETE

        # Verify that the second stage is active and has pools/matches
        assert stages[1].status == Stage.StageStatus.ACTIVE
        assert len(stages[1].pools) == 1
        assert len(stages[1].pools[0].matches) == 1
        assert stages[1].pools[0].matches[0].status == Match.MatchStatus.PENDING

        # Verify that the third stage is still pending
        assert stages[2].status == Stage.StageStatus.PENDING

    def test_progress_tournament_active_on_final_stage_completes_it_and_sets_status_to_complete(self, db):
        tournament: Tournament = TournamentFactory(status=Tournament.TournamentStatus.ACTIVE)
        stages: List[Stage] = [
            StageFactory(
                tournament=tournament,
                status=Stage.StageStatus.COMPLETE if idx < 2 else Stage.StageStatus.PENDING,
                ordinal=idx,
                params={'minimum_pool_size': 2},
            )
            for idx in range(3)
        ]
        CompetitorFactory.create_batch(2, tournament=tournament)
        stages[2].progress(db, autocommit=True)
        db.query(Match).filter(Match.pool == stages[2].pools[0]).update({Match.status: Match.MatchStatus.COMPLETE})

        tournament.progress(db, autocommit=True)

        # Verify that the tournament is now complete
        assert tournament.status == Tournament.TournamentStatus.COMPLETE

        # Verify that all stages are complete
        for stage in stages:
            assert stage.status == Stage.StageStatus.COMPLETE

    @pytest.mark.parametrize('status', [Tournament.TournamentStatus.PENDING, Tournament.TournamentStatus.COMPLETE])
    def test_progress_tournament_invalid_status_raises_error(self, db, status):
        tournament: Tournament = TournamentFactory(status=status)

        with pytest.raises(TournamentError):
            tournament.progress(db, autocommit=True)


class TestStage(DatabaseAwareTest):
    def test_progress_pending_generate_matches_and_set_to_active(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(2, tournament=stage.tournament)

        stage.progress(db, autocommit=True)

        # Verify that the status was updated
        assert stage.status == Stage.StageStatus.ACTIVE

        # Verify that pools and matches were generated
        assert len(stage.pools) == 1
        assert len(stage.pools[0].matches) == 1
        assert stage.pools[0].matches[0].status == Match.MatchStatus.PENDING

    def test_progress_active_and_all_matches_complete_set_to_complete(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(2, tournament=stage.tournament)
        stage.progress(db, autocommit=True)  # The other tests verify that this will work, so I feel ok using it here
        # Mark all the matches as complete
        db.query(Match).update({Match.status: Match.MatchStatus.COMPLETE})

        stage.progress(db, autocommit=True)

        assert stage.status == Stage.StageStatus.COMPLETE

    def test_progress_active_with_unfinished_matches_raises_error(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(2, tournament=stage.tournament)
        stage.progress(db, autocommit=True)  # The other tests verify that this will work, so I feel ok using it here

        with pytest.raises(TournamentError):
            stage.progress(db, autocommit=True)

    def test_progress_complete_raises_error(self, db):
        stage: Stage = StageFactory(status=Stage.StageStatus.COMPLETE)

        with pytest.raises(TournamentError):
            stage.progress(db, autocommit=True)

        # Verify that the status was not altered
        assert stage.status == Stage.StageStatus.COMPLETE

    def test_all_matches_complete_no_matches_raises_exception(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(2, tournament=stage.tournament)

        with pytest.raises(TournamentError):
            stage.all_matches_complete()

    def test_all_matches_complete_no_matches_complete_returns_false(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(2, tournament=stage.tournament)
        stage.progress(db, autocommit=True)

        assert not stage.all_matches_complete()

    def test_all_matches_complete_some_matches_complete_returns_false(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(3, tournament=stage.tournament)
        stage.progress(db, autocommit=True)
        stage.pools[0].matches[0].status = Match.MatchStatus.COMPLETE
        db.add(stage.pools[0].matches[0])
        db.commit()

        assert not stage.all_matches_complete()

    def test_all_matches_complete_all_matches_complete_returns_true(self, db):
        stage: Stage = StageFactory(params={'minimum_pool_size': 2})
        CompetitorFactory.create_batch(3, tournament=stage.tournament)
        stage.progress(db, autocommit=True)
        db.query(Match).update({Match.status: Match.MatchStatus.COMPLETE})

        assert stage.all_matches_complete()
