import pytest


@pytest.mark.parametrize('path', (
        '/blog/create',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "auth/login"
