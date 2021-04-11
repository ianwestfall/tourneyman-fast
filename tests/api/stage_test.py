from typing import Sequence

from database.models import Stage
from tests.conftest import not_yet_implemented
from tests.factories import TournamentFactory
from tests.utils import ApiTest


@not_yet_implemented
class TestGetStageById:
    pass


@not_yet_implemented
class TestGetStageById:
    pass


@not_yet_implemented
class TestGetStageById:
    pass


class TestUpdateStages(ApiTest):
    def test_returns_error_if_user_does_not_own_tournament(self, client, test_user, db):
        tournament = TournamentFactory(stages=3)

        response = client.put(f'/tournaments/{tournament.id}/stages/', json=[{
                'type': stage.type,
                'params': {'minimum_pool_size': 7},
            } for stage in tournament.stages
        ], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 404
        response_body = response.json()
        assert response_body == {
            'detail': f'No tournament found with id {tournament.id}',
        }

        # Verify that the stages were not altered
        db.refresh(tournament)
        for stage in tournament.stages:
            assert stage.params == {'minimum_pool_size': 5}

    def test_extra_stages_are_deleted(self, client, test_user, db):
        tournament = TournamentFactory(stages=3, owner=test_user['user'])

        response = client.put(f'/tournaments/{tournament.id}/stages/', json=[{
            'type': Stage.StageType.bracket_single_elimination,
            'params': {'seeded': True},
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]['type'] == Stage.StageType.bracket_single_elimination
        assert response_json[0]['ordinal'] == 0
        assert response_json[0]['status'] == Stage.StageStatus.pending
        assert response_json[0]['params'] == {'seeded': True}

        # Verify the DB looks ok
        stages: Sequence[Stage] = db.query(Stage).all()
        assert len(stages) == 1
        assert stages[0].tournament == tournament
        assert stages[0].ordinal == 0
        assert stages[0].type == Stage.StageType.bracket_single_elimination

    def test_new_stages_are_created_if_necessary(self, client, test_user, db):
        tournament = TournamentFactory(stages=1, owner=test_user['user'])

        response = client.put(f'/tournaments/{tournament.id}/stages/', json=[{
            'type': Stage.StageType.pool,
            'params': {'minimum_pool_size': 5},
        }, {
            'type': Stage.StageType.bracket_single_elimination,
            'params': {'seeded': True},
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 2
        assert response_json[0]['type'] == Stage.StageType.pool
        assert response_json[0]['ordinal'] == 0
        assert response_json[0]['status'] == Stage.StageStatus.pending
        assert response_json[0]['params'] == {'minimum_pool_size': 5}
        assert response_json[1]['type'] == Stage.StageType.bracket_single_elimination
        assert response_json[1]['ordinal'] == 1
        assert response_json[1]['status'] == Stage.StageStatus.pending
        assert response_json[1]['params'] == {'seeded': True}

        # Make sure the DB looks ok
        stages: Sequence[Stage] = db.query(Stage).order_by(Stage.ordinal).all()
        assert len(stages) == 2
        assert stages[0].tournament == tournament
        assert stages[0].ordinal == 0
        assert stages[0].type == Stage.StageType.pool
        assert stages[1].tournament == tournament
        assert stages[1].ordinal == 1
        assert stages[1].type == Stage.StageType.bracket_single_elimination

    def test_updates_without_length_changes_work(self, client, test_user, db):
        tournament = TournamentFactory(stages=2, owner=test_user['user'])

        response = client.put(f'/tournaments/{tournament.id}/stages/', json=[{
            'type': Stage.StageType.pool,
            'params': {'minimum_pool_size': 7},
        }, {
            'type': Stage.StageType.pool,
            'params': {'minimum_pool_size': 10},
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 2
        assert response_json[0]['type'] == Stage.StageType.pool
        assert response_json[0]['ordinal'] == 0
        assert response_json[0]['status'] == Stage.StageStatus.pending
        assert response_json[0]['params'] == {'minimum_pool_size': 7}
        assert response_json[1]['type'] == Stage.StageType.pool
        assert response_json[1]['ordinal'] == 1
        assert response_json[1]['status'] == Stage.StageStatus.pending
        assert response_json[1]['params'] == {'minimum_pool_size': 10}

        # Make sure the DB looks ok
        stages: Sequence[Stage] = db.query(Stage).order_by(Stage.ordinal).all()
        assert len(stages) == 2
        assert stages[0].tournament == tournament
        assert stages[0].ordinal == 0
        assert stages[0].type == Stage.StageType.pool
        assert stages[0].params == {'minimum_pool_size': 7}
        assert stages[1].tournament == tournament
        assert stages[1].ordinal == 1
        assert stages[1].type == Stage.StageType.pool
        assert stages[1].params == {'minimum_pool_size': 10}

    @not_yet_implemented
    def test_errors_roll_back_the_transaction(self):
        raise NotImplementedError()


@not_yet_implemented
class TestGetStage:
    pass


@not_yet_implemented
class TestDeleteStage:
    pass
