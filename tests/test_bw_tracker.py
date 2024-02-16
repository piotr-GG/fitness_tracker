import datetime

import pytest

from ft_app import DBC
from ft_app.models import BodyWeightRecord


def test_create_bw_record(app, client, auth):
    auth.login()
    assert client.get("/bw_tracker/").status_code == 200
    client.post('/bw_tracker/', data={
        "weight": 66,
        "date": datetime.date(2024, 2, 16)
    })
    db_session = DBC.get_db_session()
    result = db_session.scalars(db_session.query(BodyWeightRecord).where(BodyWeightRecord.id == 9)).one()
    assert result.weight == 66 and result.date.date() == datetime.date(2024, 2, 16)


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
@pytest.mark.parametrize('date', (
        '/bw_tracker/',
        # '/bw_tracker/plot/'
))
def test_create_bw_record_validation_failed(app, auth, date):
    assert False


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_delete_bw_record(app, auth):
    assert False


@pytest.mark.parametrize('path', (
        '/bw_tracker/',
        # '/bw_tracker/plot/'
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
