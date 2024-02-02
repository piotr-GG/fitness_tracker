from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', validators=[validators.Length(min=4, max=25)])
    email = StringField('Email Address', validators=[validators.Length(min=6, max=35)])
    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm_pass', message="Passwords must match!")
    ])
    confirm_pass = PasswordField('Repeat Password')
