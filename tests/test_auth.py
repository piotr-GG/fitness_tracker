import pytest


def test_register(client, app):
    from ft_app.models.dbc.database import db_session
    from ft_app.models.models import User
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={
        'username': 'new_user_123',
        'password': 'new_password123',
        'confirm_pass': 'new_password123',
        'email': 'newuser@gmail.com'
    })
    assert response.headers["Location"] == "auth/login"

    with app.app_context():
        q = db_session.query(User).filter(User.username == "new_user_123")
        assert db_session.execute(db_session.query(q.exists()))
