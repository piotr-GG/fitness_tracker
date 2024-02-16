import datetime

import pytest
from sqlalchemy import select

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


def test_update(client, auth):
    auth.login()
    assert client.get('blog/1/update').status_code == 200
    client.post('blog/1/update', data={
        'title': 'Updated title',
        'body': 'Updated body'
    })

    db_session = DBC.get_db_session()
    result = db_session.scalars(select(BlogPost).where(BlogPost.id == 1)).one()
    assert result.title == "Updated title" and result.body == "Updated body"


def test_delete(client, auth):
    auth.login()
    response = client.post('blog/1/delete')
    assert response.headers["Location"] == "/blog/"

    db_session = DBC.get_db_session()
    result = db_session.execute(select(BlogPost).where(BlogPost.id == 1))
    with pytest.raises(StopIteration):
        next(result.__iter__())


@pytest.mark.skip(reason="To be implemented")
def test_create_validate_form(client, auth):
    assert False


@pytest.mark.skip(reason="To be implemented")
def test_update_validate_form(client, auth):
    assert False
