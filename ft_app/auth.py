from flask import Blueprint, flash, g, redirect, request, session, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash

from ft_app.forms import RegistrationForm

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
        flash("Muchas gracias por registrarte!")
        return redirect(url_for('auth.login'))
    return render_template("auth/register.html", form=form)
