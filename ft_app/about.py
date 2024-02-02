from flask import Blueprint, render_template, request
from ft_app.models.dbc.database import db_session

bp = Blueprint("about", __name__, url_prefix="/about")


@bp.route('/')
def index():
    return render_template("about/index.html")
