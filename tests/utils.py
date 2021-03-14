import pytest
from fastapi.testclient import TestClient

from api.routers.security import create_access_token
from main import app
from tests.conftest import Session
from tests.factories import UserFactory


class ApiTestClass:
    @pytest.fixture(autouse=True)
    def client(self):
        yield TestClient(app)

    @pytest.fixture
    def db(self):
        session = Session()
        try:
            yield session
        finally:
            Session.remove()

    @pytest.fixture(autouse=True)
    def test_user(self, db):
        db_user = UserFactory()
        auth_token = create_access_token(data={'sub': db_user.email})
        yield {
            'user': db_user,
            'auth_token': auth_token,
        }
