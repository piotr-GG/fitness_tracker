import datetime
import math

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


@pytest.mark.parametrize(('date', 'weight'), (
        (datetime.date.today(), 25),
        (datetime.date.today(), 205),
        (datetime.date.today() + datetime.timedelta(days=2), 35),
        (datetime.date.today() + datetime.timedelta(days=2), 198),
        (datetime.date.today() + datetime.timedelta(days=2), 29.99),
        (datetime.date.today() + datetime.timedelta(days=2), 199.99)
))
def test_create_bw_record_validation_failed(app, client, auth, date, weight):
    auth.login()
    assert client.get("/bw_tracker/").status_code == 200
    client.post('/bw_tracker/', data={
        "weight": weight,
        "date": date
    })
    db_session = DBC.get_db_session()
    result = db_session.scalars(db_session.query(BodyWeightRecord).order_by(BodyWeightRecord.id))
    last_record = result.all()[-1]
    assert last_record.weight != weight and last_record.date.date() != date


def test_update_bw_record(app, client, auth):
    auth.login()
    response = client.post('bw_tracker/update/1',
                           data={
                               "weight": 75
                           })
    assert response.headers["Location"] == "/bw_tracker/"
    db_session = DBC.get_db_session()
    result = db_session.scalars(select(BodyWeightRecord).where(BodyWeightRecord.id == 1)).one()
    assert result.weight == 75


@pytest.mark.parametrize('weight', (
        24.99,
        200.1
))
def test_update_bw_record_validation_failed(app, client, auth, weight):
    auth.login()
    client.post('bw_tracker/update/1',
                data={
                    "weight": weight
                })
    db_session = DBC.get_db_session()
    result = db_session.scalars(select(BodyWeightRecord).where(BodyWeightRecord.id == 1)).one()
    assert not math.isclose(result.weight, weight)


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


def test_delete_bw_record(app, client, auth):
    auth.login()
    response = client.post('bw_tracker/delete/1')
    assert response.headers["Location"] == "/bw_tracker/"

    db_session = DBC.get_db_session()
    result = db_session.execute(select(BodyWeightRecord).where(BodyWeightRecord.id == 1))
    with pytest.raises(StopIteration):
        next(result.__iter__())


# @pytest.mark.skip(reason="TO BE IMPLEMENTED")
# def test_plot(app, auth):
#     assert False
