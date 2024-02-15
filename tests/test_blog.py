import datetime

import pytest

from ft_app import DBC
from ft_app.models import BlogPost


def test_blog_index(client, auth):
    response = client.get('/blog/')
    assert b"Welcome to the blog!" in response.data

    auth.login()
    response = client.get('/blog/')
    assert b"New post" in response.data


@pytest.mark.parametrize('path', (
        '/blog/create',
        '/blog/1/update',
        '/blog/1/delete'
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_create(client, auth, app):
    auth.login()
    assert client.get('/blog/create').status_code == 200

    client.post('/blog/create',
                data={
                    "date": datetime.datetime.utcnow().date(),
                    "title": "Testing 101!",
                    "body": "This is a test post!"
                })

    db_session = DBC.get_db_session()
    result = db_session.scalars(db_session.query(BlogPost).where(BlogPost.id == 3))
    assert result.one()


def test_create_not_moderator(client, auth, app):
    auth.login(username="user_1234", password="user_1234")
    assert client.get('/blog/create').status_code == 403
