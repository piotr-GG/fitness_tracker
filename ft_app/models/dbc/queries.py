from collections import namedtuple

from sqlalchemy import select

from ft_app.models.dbc.database import db_session
from ft_app.models.models import User, BlogPost, BodyWeightRecord


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
    Result = namedtuple('BlogPostData', ['post', 'user'])
    results = []
    db_data = db_session.execute(select(BlogPost, User).where(BlogPost.user_id == User.id).order_by(BlogPost.user_id))
    for r in db_data:
        results.append(Result(r[0], r[1]))
    return reversed(results)


def get_post_by_id(post_id):
    return db_session.scalars(select(BlogPost).where(BlogPost.id == post_id)).one()


def get_bw_records_by_id(user_id):
    return db_session.scalars(select(BodyWeightRecord).where(BodyWeightRecord.user_id == user_id)).all()