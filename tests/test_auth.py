import pytest
from flask import session

from ft_app import DBC
from ft_app.models import User


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={
        'username': 'new_user_123',
        'password': 'new_password123',
        'confirm_pass': 'new_password123',
        'email': 'newuser@gmail.com'
    })
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        db_session = DBC.get_db_session()
        q = db_session.query(User).filter(User.username == "new_user_123")
        assert db_session.execute(db_session.query(q.exists()))


def test_login(client, app):
    assert client.get('/auth/login').status_code == 200
    response = client.post('/auth/login', data={
        'username': 'test_1234',
        'password': 'test_1234'
    })
    assert response.headers["Location"] == "/"
    with client:
        client.get('/')
        assert session['user_id'] == 1


@pytest.mark.parametrize(("username", "password", "message"), (
        ("test_12345", "test_1234", b"Incorrect username"),
        ("test_1234", "test_xyz", b"Incorrect password")))
def test_login_failed(client, app, username, password, message):
    assert client.get('/auth/login').status_code == 200
    response = client.post('/auth/login', data={
        "username": username,
        "password": password
    })
    assert message in response.data
    with client:
        client.get('/')
        assert session.get('user_id', None) is None


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert session.get('user_id', None) is None


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
@pytest.mark.parametrize(('username', 'password', 'email', 'message'), (
        ('', '', '', b"TO BE FILLED"),
        ('testing_101', '', '', b"TO BE FILLED"),
        ('test_1234', 'test_1234', "test_1234@gmail.com", b"TO BE FILLED"),
        ('test_XYZ', 'test_XYZ', "test_1234@gmail.com", b"TO BE FILLED")
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/auth/register',
        data={
            'username': username,
            'password': password,
            'email': email
        })
    assert message in response.data


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_login_while_logged_in(client, auth):
    auth.login()
    assert client.get('/auth/login').status_code == 421
