import datetime
import os

import pytest
import tempfile

from ft_app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })
    print("DB PATH: ", db_path)

    with app.app_context():
        from ft_app.models.dbc.database import init_db
        init_db()

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


def create_test_data():
    from ft_app.models.models import User, BodyWeightRecord, BlogPost
    from ft_app.models.dbc.database import db_session

    db_session.add(User(username="adrian", password="1234567", email="ceo@gmail.com", is_moderator=True))
    db_session.add(User(username="ganesh", password="ganesh", email="ganesh@gmail.com"))

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
