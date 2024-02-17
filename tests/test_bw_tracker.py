import datetime

import pytest
from sqlalchemy import select

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


def test_delete_bw_record(app, client, auth):
    auth.login()
    response = client.post('bw_tracker/delete/1')
    assert response.headers["Location"] == "/bw_tracker/"

    db_session = DBC.get_db_session()
    result = db_session.execute(select(BodyWeightRecord).where(BodyWeightRecord.id == 1))
    with pytest.raises(StopIteration):
        next(result.__iter__())


def test_update_bw_record(app, client, auth):
    pass


@pytest.mark.parametrize('path', (
        '/bw_tracker/',
        # '/bw_tracker/plot/'
))
def test_login_required(app, client, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"


def test_delete_bw_record_other_than_yours(app, auth, client):
    auth.login()
    response = client.post('bw_tracker/delete/5')
    assert response.status_code == 403


@pytest.mark.skip(reason="TO BE IMPLEMENTED")
def test_plot(app, auth):
    assert False
