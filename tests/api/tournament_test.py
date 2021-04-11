import json
from datetime import datetime, timedelta

from api.schemas.tournament import TournamentList
from database.models import Tournament
from tests.factories import TournamentFactory
from tests.utils import ApiTest


# noinspection PyMethodMayBeStatic
class TestTournament(ApiTest):
    def test_create_tournament(self, client, test_user, db):
        test_start_date = datetime.now().isoformat()
        response = client.post('/tournaments/', json={
            'name': 'Test Tournament',
            'organization': 'CKDF',
            'start_date': test_start_date,
            'public': True,
        }, headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify that the response was correct
        assert response.status_code == 201
        response_body = response.json()
        assert response_body['name'] == 'Test Tournament'
        assert response_body['organization'] == 'CKDF'
        assert response_body['start_date'] == test_start_date
        assert response_body['public'] is True

        # Verify that the DB was updated
        tournaments = db.query(Tournament).all()
        assert len(tournaments) == 1
        tournament = tournaments[0]
        assert tournament.id is not None
        assert tournament.name == 'Test Tournament'
        assert tournament.organization == 'CKDF'
        assert tournament.start_date == datetime.fromisoformat(test_start_date)
        assert tournament.status == Tournament.TournamentStatus.pending
        assert tournament.public is True
        assert tournament.owner == test_user['user']
        assert tournament.competitors == []
        assert tournament.stages == []

    def test_get_tournaments_not_filtered_and_no_public_tournaments_returns_nothing(self, client, test_user, db):
        # Create a private tournament from a different user
        TournamentFactory()

        response = client.get('/tournaments/', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert response_body['total'] == 0
        assert response_body['items'] == []

    def test_get_tournaments_not_filtered_and_some_tournaments_returns_public_tourneys(self, client, test_user, db):
        # Create some private and two public tournaments from different users
        TournamentFactory()
        private_tournament = TournamentFactory(owner=test_user['user'], start_date=datetime.now() + timedelta(days=3))
        public_tournaments = [
            TournamentFactory(public=True, start_date=datetime.now() + timedelta(days=2)),
            TournamentFactory(public=True),
        ]

        response = client.get('/tournaments/', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        assert response.status_code == 200
        response_body = response.json()
        assert response_body == json.loads(TournamentList(**{
            'total': 3,
            'items': [private_tournament] + public_tournaments,
        }).json())

    def test_get_tournaments_filtered_and_no_public_tournaments_returns_nothing(self, client, test_user, db):
        # Create a private factory from a different user
        TournamentFactory()

        response = client.get('/tournaments/?is_filtered_by_user=true', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert response_body['total'] == 0
        assert response_body['items'] == []

    def test_get_tournaments_filtered_and_some_tournaments_returns_public_and_users_private_tourneys(
            self, client, test_user, db,
    ):
        # Create some private and two public tournaments from different users
        TournamentFactory()
        private_tournament = TournamentFactory(owner=test_user['user'], start_date=datetime.now() + timedelta(days=3))
        _public_tournaments = [
            TournamentFactory(public=True, start_date=datetime.now() + timedelta(days=2)),
            TournamentFactory(public=True),
        ]

        response = client.get('/tournaments/?is_filtered_by_user=true', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == json.loads(TournamentList(**{
            'total': 1,
            'items': [private_tournament],
        }).json())

    def test_get_tournaments_pagination_limits_result_set(self, client, test_user, db):
        test_tournaments = [
            TournamentFactory.create(
                public=True,
                start_date=datetime.now() + timedelta(days=i),
            ) for i in range(25)
        ]
        test_tournaments.reverse()

        # Grab the first page for a page size of 10
        response = client.get('/tournaments/?skip=0&limit=10', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == json.loads(TournamentList(**{
            'total': 25,
            'items': test_tournaments[0:10],
        }).json())

        # Grab the second page for a page size of 10
        response = client.get('/tournaments/?skip=10&limit=10', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == json.loads(TournamentList(**{
            'total': 25,
            'items': test_tournaments[10:20],
        }).json())

        # Grab the third page for a page size of 10, which will be a partial page
        response = client.get('/tournaments/?skip=20&limit=10', headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        # Verify the response
        assert response.status_code == 200
        response_body = response.json()
        assert response_body == json.loads(TournamentList(**{
            'total': 25,
            'items': test_tournaments[20:],
        }).json())
