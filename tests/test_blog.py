import pytest


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

