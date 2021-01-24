from datetime import datetime

from tests.utils import ApiTestClass


# noinspection PyMethodMayBeStatic
class TestTournament(ApiTestClass):
    def test_create_tournament(self, client, test_user):
        test_start_date = datetime.now().isoformat()
        response = client.post('/tournaments/', json={
            'name': 'Test Tournament',
            'organization': 'CKDF',
            'start_date': test_start_date,
            'public': True,
        }, headers={
            'Authorization': f'Bearer {test_user["auth_token"]}'
        })

        assert response.status_code == 201
        response_body = response.json()
        assert response_body['name'] == 'Test Tournament'
        assert response_body['organization'] == 'CKDF'
        assert response_body['start_date'] == test_start_date
        assert response_body['public'] is True
