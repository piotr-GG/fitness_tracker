import datetime

import pytest

from ft_app.forms import RegistrationForm, BodyWeightRecordForm, BlogPostCreateForm, LoginForm


@pytest.mark.parametrize(('username', 'email', 'password', 'result'),
                         (
                                 ('username', 'email@email.com', 'password', True),
                                 ('use', 'email@email.com', 'password', False),
                                 ('username_is_really_to_long_in_here', 'email@email.com', 'password', False),

                                 ('username', 'e@e.pl', 'password', False),
                                 ('username', 'really_long_email_in_here@long_domain.com', 'password', False),
                                 ('username', 'not_an_email.com', 'password', False),

                                 ('username', 'email@email.com', '', False),
                                 ('username', 'email@email.com', 'short', False),
                                 ('username', 'email@email.com', 'very_long_password_that_is_long', False),
                         ))
def test_registration_form(app, username, email, password, result):
    form = RegistrationForm()
    form.username.data = username
    form.email.data = email
    form.password.data = password
    form.confirm_pass.data = password
    assert form.validate() == result


def test_registration_form_confirm_pass():
    form = RegistrationForm()
    form.username.data = 'username'
    form.email.data = 'email@email.com'
    form.password.data = 'password'
    form.confirm_pass.data = 'different_password'
    assert not form.validate()


@pytest.mark.parametrize(('username', 'password', 'result'),
                         (
                                 ('username', 'password', True),
                                 ('', 'password', False),  # Empty username should fail
                                 ('username', '', False),  # Empty password should fail
                                 ('', '', False),  # Both empty fields should fail
                         ))
def test_login_form(username, password, result):
    form = LoginForm()
    form.username.data = username
    form.password.data = password
    assert form.validate() == result


@pytest.mark.parametrize(('date', 'title', 'body', 'result'),
                         (
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), 'Title', 'Blog post body', True),  # Valid data
                                 ('', 'Title', 'Blog post body', False),  # Empty date should fail
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), '', 'Blog post body', False),  # Empty title should fail
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), 'Title', '', False),  # Empty body should fail
                         ))
def test_blog_post_create_form(date, title, body, result):
    form = BlogPostCreateForm()
    form.date.data = date
    form.title.data = title
    form.body.data = body
    assert form.validate() == result


@pytest.mark.parametrize(('date', 'weight', 'result'),
                         (
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), 70, True),  # Valid data
                                 ('', 70, False),  # Empty date should fail
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), 0, False),  # Empty weight should fail
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), 10, False),  # Weight below range should fail
                                 (datetime.datetime.strptime('2024-02-18', "%Y-%m-%d").date(), 250, False),  # Weight above range should fail
                         ))
def test_body_weight_record_form(date, weight, result):
    form = BodyWeightRecordForm()
    form.date.data = date
    form.weight.data = weight
    assert form.validate() == result
