import json
from datetime import datetime, timedelta

import factory
from factory import post_generation

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

    @post_generation
    def stages(self, create, extracted, **kwargs):
        if create and extracted:
            for i in range(extracted):
                StageFactory(tournament=self, ordinal=i, **kwargs)

    @post_generation
    def competitors(self, create, extracted, **kwargs):
        if create and extracted:
            for i in range(extracted):
                CompetitorFactory(tournament=self, **kwargs)


class StageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Stage
        sqlalchemy_session = conftest.Session
        sqlalchemy_session_persistence = "commit"

    tournament = factory.SubFactory(TournamentFactory)
    ordinal = 0
    type = models.Stage.StageType.pool
    status = models.Stage.StageStatus.pending
    params = {'minimum_pool_size': 5}


class CompetitorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Competitor
        sqlalchemy_session = conftest.Session
        sqlalchemy_session_persistence = "commit"

    tournament = factory.SubFactory(TournamentFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    organization = factory.Faker('company')
    location = factory.Faker('city')

