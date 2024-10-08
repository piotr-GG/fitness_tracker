import datetime
from datetime import date

from wtforms import Form, StringField, PasswordField, validators, TextAreaField
from wtforms.fields.datetime import DateField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import StopValidation
from flask_wtf import FlaskForm


# TODO: Create new dir for forms only and separate custom validators into another Python module
def validate_date_not_in_future(form, field):
    if field.data > datetime.datetime.utcnow().date():
        raise StopValidation("Cannot create blog post with date set in future!")


def validate_bw_record(form, field):
    print(field.data)
    print(type(field.data))
    value_low = 30
    value_high = 200
    if not (value_low <= field.data <= value_high):
        raise StopValidation(f"Body weight records are only allowed to be within {value_low} and {value_high} range!")


class FormErrorPrinter(Form):
    def print_error_message(self):
        rows = []
        for i in self.errors.items():
            field_name, err_msg = i
            msgs = " ; ".join(err_msg)
            rows.append(": ".join([field_name, msgs]))
        return rows


class RegistrationForm(FormErrorPrinter):
    username = StringField('Username', validators=[validators.Length(min=4, max=25)])
    email = StringField('Email Address', validators=[
        validators.Length(min=8, max=35),
        validators.Email(message="Provided e-mail is not a valid e-mail address", check_deliverability=False)])
    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=25, message="Password must be between 6 and 25 characters long."),
        validators.EqualTo('confirm_pass', message="Passwords must match!")
    ])
    confirm_pass = PasswordField('Repeat Password')


class LoginForm(FormErrorPrinter):
    username = StringField('Username',
                           validators=[validators.DataRequired()])
    password = PasswordField("Password",
                             validators=[validators.DataRequired()])


class BlogPostCreateForm(FormErrorPrinter):
    date = DateField('Date added',
                     default=date.today(),
                     validators=[validators.DataRequired(),
                                 validate_date_not_in_future])
    title = StringField('Title',
                        validators=[validators.Length(min=5, max=200)],
                        render_kw={"class": "resizable-text-title"})
    body = TextAreaField('Body',
                         validators=[validators.Length(min=5)],
                         render_kw={"class": "resizable-text-body"})


class BodyWeightRecordForm(FormErrorPrinter):
    date = DateField('Date',
                     default=date.today(),
                     validators=[validators.DataRequired(),
                                 validate_date_not_in_future])
    weight = DecimalField('Weight',
                          validators=[validators.DataRequired(), validate_bw_record])


class ExerciseRecordForm(FormErrorPrinter):
    ex_id = HiddenField('Exercise ID')
    exercise_name = StringField('Exercise Name',
                                validators=[],
                                render_kw={"readonly": "readonly"}
                                )
    sets = StringField('Sets', validators=[validators.DataRequired()])
    reps = StringField('Reps', validators=[validators.DataRequired()])


class ExerciseMainForm(FlaskForm):
    exercises = FieldList(FormField(ExerciseRecordForm))
    submit = SubmitField("Save All")
