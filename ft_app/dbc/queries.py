from sqlalchemy import select

from ft_app.dbc.database import DBC
from ft_app.models import User, BlogPost, BodyWeightRecord

db_session = DBC.db_session


def check_if_user_exists(user: User):
    for fun, msg in zip([_user_exists_by_username, _user_exists_by_email], ["login", "email"]):
        result = fun(user).fetchone()
        if result[0]:
            return True, f"User with given {msg} is already registered!"
    return False, ""


def _user_exists_by_username(user: User):
    q = db_session.query(User).filter(User.username == user.username)
    return db_session.execute(db_session.query(q.exists()))


def _user_exists_by_email(user: User):
    q = db_session.query(User).filter(User.email == user.email)
    return db_session.execute(db_session.query(q.exists()))


def get_user_by_id(user_id):
    return db_session.execute(select(User).where(User.id == user_id)).fetchone().User


def get_all_posts():
    return reversed(db_session.scalars(select(BlogPost).order_by(BlogPost.date)).all())


def get_post_by_id(post_id):
    return db_session.scalars(select(BlogPost).where(BlogPost.id == post_id)).one()


def get_bw_records_by_id(user_id):
    return (db_session.scalars(
        select(BodyWeightRecord)
        .where(BodyWeightRecord.user_id == user_id)
        .order_by(BodyWeightRecord.date))
            .all())
