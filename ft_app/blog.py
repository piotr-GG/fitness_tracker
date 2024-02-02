from flask import Blueprint, redirect, render_template, request
from ft_app.models.dbc.database import db_session

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("blog/index.html")
