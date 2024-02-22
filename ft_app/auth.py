import functools

from flask import Blueprint, flash, g, redirect, request, session, url_for, render_template
from sqlalchemy import select
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash

from ft_app import DBC
from ft_app.forms import RegistrationForm, LoginForm
from ft_app.dbc.queries import check_if_user_exists, get_user_by_id
from ft_app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/user_panel', methods=['GET', 'POST'])
def user_panel():
    return render_template("auth/user_panel.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if session.get('user_id') is not None:
        abort(403)

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db_session = DBC.get_db_session()
        user = db_session.execute(select(User).where(User.username == username)).fetchone()
        error = None

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(user.User.password, password):
            error = "Incorrect password."
        else:
            user = user.User

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash("You have been successfully logged in!")
            return redirect(url_for('index'))
        else:
            flash(error)
    return render_template("auth/login.html", form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if session.get('user_id') is not None:
        abort(403)

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
                db_session = DBC.get_db_session()
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


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        if not hasattr(g, "user") or g.user is None or g.user.id != user_id:
            g.user = get_user_by_id(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect((url_for('index')))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
