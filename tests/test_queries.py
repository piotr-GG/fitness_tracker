import pytest
from ft_app.models import User
from ft_app.dbc.queries import check_if_user_exists, _user_exists_by_username, _user_exists_by_email, get_user_by_id, \
    get_all_posts, get_post_by_id, get_bw_records_by_id


@pytest.mark.parametrize(("user_name", "email", "expected"), (
        ("test_1234", "test_1234@gmail.com", True),
        ("test_1234", "other@gmail.com", True),
        ("other_1234", "test_1234@gmail.com", True),
        ("other_1234", "other_1234@gmail.com", False)
))
def test_check_if_user_exists(app, user_name, email, expected):
    user = User(username=user_name, password="test_1234", email=email)
    status, msg = check_if_user_exists(user)
    assert status is expected


@pytest.mark.parametrize(("user_name", "expected"), (
        ("test_1234", True),
        ("user_1234", True),
        ("random_guy", False),
        ("test_12345", False)
))
def test_user_exists_by_username(app, user_name, expected):
    user = User(username=user_name, password="test_1234", email="test_1234@gmail.com")
    result = _user_exists_by_username(user).fetchone()
    assert result[0] is expected


@pytest.mark.parametrize(("email", "expected"), (
        ("test_1234@gmail.com", True),
        ("user@gmail.com", True),
        ("random_guy@gmail.com", False),
        ("test_12345@gmail.com", False)
))
def test_user_exists_by_email(app, email, expected):
    user = User(username="testing_user", password="test_1234", email=email)
    result = _user_exists_by_email(user).fetchone()
    assert result[0] is expected


@pytest.mark.parametrize(("user_id", "expected"), (
        (1, True),
        (2, True),
        # (-1, False),
        # (3, False)
))
def test_get_user_by_id(app, user_id, expected):
    result = get_user_by_id(user_id)
    assert result is not None


def test_get_all_posts(app):
    result = get_all_posts()
    assert result is not None


@pytest.mark.parametrize(("post_id", "expected"), (
        (1, True),
        (2, True),
        # (-1, False),
        # (3, False)
))
def test_get_post_by_id(app, post_id, expected):
    blog_post = get_post_by_id(post_id)
    assert (blog_post is not None) is expected


@pytest.mark.parametrize(("user_id", "expected"), (
        (1, True),
        (2, True),
        # (-1, False),
        # (3, False)
))
def test_get_bw_records_by_id(app, user_id, expected):
    blog_posts = get_bw_records_by_id(user_id)
    assert (blog_posts is not None) is expected
