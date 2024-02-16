import pytest


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_create_bw_record(app, auth):
    assert False


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_delete_bw_record(app, auth):
    assert False


@pytest.mark.parametrize('path', (
        '/bw_tracker',
        'bw_tracker/plot'
))
def test_login_required(app, client, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_delete_bw_record_other_than_yours(app, auth):
    assert False


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_plot(app, auth):
    assert False
