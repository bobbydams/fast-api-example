import sqlite3

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.api.adapters import orm
from apps.api.domain import model


def init_mock_data(session):
    session.query(model.Book).delete()
    session.query(model.Tag).delete()


@pytest.fixture
def client():
    from apps.api.entrypoint import app

    yield TestClient(app)


@pytest.fixture
def in_memory_sqlite_db():
    DB_URI = "file::memory:?cache=shared"
    creator = lambda: sqlite3.connect(DB_URI, uri=True)
    engine = create_engine("sqlite:///:memory:", creator=creator)
    orm.metadata.drop_all(engine)
    orm.metadata.create_all(engine)
    yield engine
    orm.metadata.drop_all(engine)


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)