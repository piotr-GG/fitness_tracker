from wtforms import Form, BooleanField, StringField, PasswordField, validators

from ft_app.models.dbc.database import db_session
from ft_app.models.models import User


class RegistrationForm(Form):
    username = StringField('Username', validators=[validators.Length(min=4, max=25)])
    email = StringField('Email Address', validators=[validators.Length(min=6, max=35)])
    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm_pass', message="Passwords must match!")
    ])
    confirm_pass = PasswordField('Repeat Password')

    def exits_username(self, username):
        q = db_session.query(User).filter(User.username == username)
        is_already_present = db_session.query(q.exists())
        return is_already_present

