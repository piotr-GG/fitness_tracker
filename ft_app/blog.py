from flask import Blueprint, redirect, render_template, request
from ft_app.models.dbc.database import db_session
from ft_app.models.dbc.queries import get_all_posts

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route('/', methods=["POST", "GET"])
def index():
    posts = get_all_posts().fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route('/create', methods=["POST", "GET"])
def create():
    return "Poczekajcie!"
