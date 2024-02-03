import sqlite3

from flask import Blueprint, flash, g, redirect, request, session, url_for, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from ft_app.forms import RegistrationForm
from ft_app.models.dbc.database import db_session
from ft_app.models.dbc.queries import check_if_user_exists
from ft_app.models.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/user_panel', methods=['GET', 'POST'])
def user_panel():
    return render_template("auth/user_panel.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("auth/login.html")


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST":
        if form.validate():
            new_user = User(username=request.form['username'],
                            password=request.form['password'],
                            email=request.form['email'])

            is_already_present, msg = check_if_user_exists(new_user)

            if is_already_present:
                flash(msg)
                return render_template("auth/register.html", form=form)

            try:
                db_session.add(new_user)
                db_session.commit()
            except Exception as e:
                return e

            flash("User account has been successfully created!")
            return redirect(url_for('auth.login'))
        else:
            msg = form.print_error_message()
            flash(r"There were errors during registration. Please correct them.")
            for m in msg:
                flash(m)
    return render_template("auth/register.html", form=form)
