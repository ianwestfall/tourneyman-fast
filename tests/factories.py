from datetime import datetime, timedelta

import factory

from database import models
from tests import conftest


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = conftest.Session
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker('email')
    password = factory.Faker('word')


class TournamentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Tournament
        sqlalchemy_session = conftest.Session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker('sentence')
    organization = factory.Faker('word')
    start_date = datetime.now() + timedelta(days=1)
    owner = factory.SubFactory(UserFactory)
