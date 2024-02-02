from flask import Blueprint, flash, g, redirect, request, session, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/user_panel', methods=['GET', 'POST'])
def user_panel():
    return render_template("auth/user_panel.html")



@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("auth/login.html")


@bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("auth/register.html")
