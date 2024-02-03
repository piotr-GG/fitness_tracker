import sqlite3

from flask import Blueprint, flash, g, redirect, request, session, url_for, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from ft_app.forms import RegistrationForm
from ft_app.models.dbc.database import db_session
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
    if request.method == "POST" and form.validate():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)

        # db_session.add(new_user)
        q = db_session.query(User).filter(User.username == username)
        is_already_present = db_session.execute(db_session.query(q.exists())).fetchone()
        print(is_already_present[0])
        if is_already_present[0]:
            flash("User with given login is already registered!")
        else:
            flash("Everything is fine!")
        return redirect(url_for('auth.login'))
        # db_session.commit()
        #
        # try:
        #     pass
        # except IntegrityError:
        #     flash("User with given login is already registered!")
        #     return redirect(url_for('auth.login'))
            # return render_template("auth/register.html", form=form)
        # flash("Muchas gracias por registrarte!")
        return redirect(url_for('auth.login'))
    return render_template("auth/register.html", form=form)
