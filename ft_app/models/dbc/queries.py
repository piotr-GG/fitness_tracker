from sqlalchemy import select

from ft_app.models.dbc.database import db_session
from ft_app.models.models import User, BlogPost


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
    q = db_session.query(BlogPost).all()
    return db_session.execute(db_session.query(q))
