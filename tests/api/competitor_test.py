from typing import Sequence

from database.models import Competitor
from tests.conftest import not_yet_implemented
from tests.factories import TournamentFactory
from tests.utils import ApiTest


@not_yet_implemented
class TestGetCompetitorById:
    pass


@not_yet_implemented
class TestCreateCompetitor:
    pass


@not_yet_implemented
class TestCreateCompetitors:
    pass


@not_yet_implemented
class TestGetCompetitors:
    pass


class TestUpdateCompetitors(ApiTest):
    def test_wrong_owner_gets_404(self, client, test_user, db):
        tournament = TournamentFactory()

        response = client.put(f'/tournaments/{tournament.id}/competitors/', json=[{
            'organization': 'Org 1',
        }, {
            'organization': 'Org 2',
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 404
        response_body = response.json()
        assert response_body == {
            'detail': f'No tournament found with id {tournament.id}',
        }

    def test_none_exist_new_ones_created(self, client, test_user, db):
        tournament = TournamentFactory(owner=test_user['user'])

        response = client.put(f'/tournaments/{tournament.id}/competitors/', json=[{
            'organization': 'Org 1',
        }, {
            'organization': 'Org 2',
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert len(response_body) == 2
        assert response_body[0]['first_name'] is None
        assert response_body[0]['last_name'] is None
        assert response_body[0]['organization'] == 'Org 1'
        assert response_body[0]['location'] is None
        assert response_body[1]['first_name'] is None
        assert response_body[1]['last_name'] is None
        assert response_body[1]['organization'] == 'Org 2'
        assert response_body[1]['location'] is None

        # Verify the DB
        competitors: Sequence[Competitor] = db.query(Competitor).order_by(Competitor.organization).all()
        assert len(competitors) == 2
        assert competitors[0].tournament == tournament
        assert competitors[0].first_name is None
        assert competitors[0].last_name is None
        assert competitors[0].organization == 'Org 1'
        assert competitors[0].location is None
        assert competitors[1].tournament == tournament
        assert competitors[1].first_name is None
        assert competitors[1].last_name is None
        assert competitors[1].organization == 'Org 2'
        assert competitors[1].location is None

    def test_old_ones_deleted_new_ones_created(self, client, test_user, db):
        tournament = TournamentFactory(owner=test_user['user'], competitors=10)

        response = client.put(f'/tournaments/{tournament.id}/competitors/', json=[{
            'organization': 'Org 1',
        }, {
            'organization': 'Org 2',
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert len(response_body) == 2
        assert response_body[0]['first_name'] is None
        assert response_body[0]['last_name'] is None
        assert response_body[0]['organization'] == 'Org 1'
        assert response_body[0]['location'] is None
        assert response_body[1]['first_name'] is None
        assert response_body[1]['last_name'] is None
        assert response_body[1]['organization'] == 'Org 2'
        assert response_body[1]['location'] is None

        # Verify the DB
        competitors: Sequence[Competitor] = db.query(Competitor).order_by(Competitor.organization).all()
        assert len(competitors) == 2
        assert competitors[0].tournament == tournament
        assert competitors[0].first_name is None
        assert competitors[0].last_name is None
        assert competitors[0].organization == 'Org 1'
        assert competitors[0].location is None
        assert competitors[1].tournament == tournament
        assert competitors[1].first_name is None
        assert competitors[1].last_name is None
        assert competitors[1].organization == 'Org 2'
        assert competitors[1].location is None

    def test_integrity_error_rollsback_all_changes(self, client, test_user, db):
        tournament = TournamentFactory(owner=test_user['user'], competitors=10)

        response = client.put(f'/tournaments/{tournament.id}/competitors/', json=[{
            'organization': 'Org 1',
        }, {
            'organization': 'Org 2',
        }, {
            'first_name': 'test_user',
        }], headers={
            'Authorization': f'Bearer {test_user["auth_token"]}',
        })

        # Verify the response
        assert response.status_code == 409
        assert response.json() == {'detail': 'Competitors must have at least a last name or an organization'}

        # Verify the DB
        competitors: Sequence[Competitor] = db.query(Competitor).filter(Competitor.tournament == tournament).all()
        assert len(competitors) == 10


@not_yet_implemented
class TestGetCompetitor:
    pass


@not_yet_implemented
class TestUpdateCompetitor:
    pass


@not_yet_implemented
class TestDeleteCompetitor:
    pass
