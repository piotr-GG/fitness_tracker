import datetime
import os
import pytest
import tempfile

from ft_app import create_app
from ft_app.dbc.database import DBC
from ft_app.models import User, BodyWeightRecord, BlogPost


@pytest.fixture(scope="session")
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        DBC.create_engine()
        DBC.create_db_session()
        DBC.init_db()

    with app.app_context():
        create_test_data()
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_1234', password='test_1234'):
        return self._client.post(
            '/auth/login',
            data={'username': username,
                  'password': password}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)


def create_test_data():
    db_session = DBC.get_db_session()
    db_session.add(User(username="test_1234", password="test_1234", email="test_1234@gmail.com", is_moderator=True))
    db_session.add(User(username="user_1234", password="user_1234", email="user@gmail.com"))

    db_session.add(BodyWeightRecord(weight=90.5, date="2023-01-01", user_id=1))
    db_session.add(BodyWeightRecord(weight=91.2, date="2023-01-02", user_id=1))
    db_session.add(BodyWeightRecord(weight=92.5, date="2023-01-03", user_id=1))
    db_session.add(BodyWeightRecord(weight=95.5, date="2023-01-04", user_id=1))

    db_session.add(BodyWeightRecord(weight=68.5, date="2023-02-01", user_id=2))
    db_session.add(BodyWeightRecord(weight=71.2, date="2023-02-02", user_id=2))
    db_session.add(BodyWeightRecord(weight=65.5, date="2023-02-03", user_id=2))
    db_session.add(BodyWeightRecord(weight=67.5, date="2023-02-04", user_id=2))

    db_session.add(BlogPost(date=datetime.datetime.utcnow(),
                            title="yyyy, eee, yyy",
                            body="Poczekajcie, muszę pomyśleć!",
                            user_id=1))

    db_session.add(BlogPost(date=datetime.datetime.utcnow(),
                            title="Jestem największym koksem",
                            body="Jestem Szefem, ja jestem Szefem!",
                            user_id=1))
    db_session.commit()
