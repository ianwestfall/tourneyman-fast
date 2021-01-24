import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('.')

from database.db import Base, get_db
from main import app
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

test_db_conn_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
test_db_name = f'{DB_NAME}_test'

engine = create_engine(test_db_conn_string)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
try:
    session_local.connection().connection.set_isolation_level(0)
    session_local.execute(f'drop database if exists {test_db_name}')
    session_local.execute(f'create database {test_db_name}')
finally:
    session_local.close()

engine = create_engine(f'{test_db_conn_string}/{test_db_name}')
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def connection():
    return engine.connect()


@pytest.fixture(scope='function', autouse=True)
def setup_database(connection):
    """
    This builds all the tables from the models (not from the migrations) before each test and tears them down after each
    test. This is almost definitely going to be extremely slow, but getting nested transactions around each test working
    was unsuccessful.
    """
    Base.metadata.bind = connection
    Base.metadata.create_all()

    def override_get_db():
        test_db = session_local()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    Base.metadata.drop_all()
