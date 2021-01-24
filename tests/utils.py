import pytest
from fastapi.testclient import TestClient

from api.routers.security import create_access_token
from api.schemas.security import UserCreate
from database.models import User
from main import app
from tests.conftest import session_local


class ApiTestClass:
    @pytest.fixture(autouse=True)
    def client(self):
        yield TestClient(app)

    @pytest.fixture(autouse=True)
    def test_user(self):
        session = session_local()

        try:
            uc = UserCreate(
                email='user@test.com',
                password='pa$$word',
            )
            db_user = User.create(uc, session)
            auth_token = create_access_token(data={'sub': db_user.email})
            yield {
                'user': db_user,
                'auth_token': auth_token,
            }
        finally:
            session.close()
