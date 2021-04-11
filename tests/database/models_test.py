from database.models import Tournament, Stage
from tests.factories import TournamentFactory
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
