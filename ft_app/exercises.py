from flask import Blueprint, flash, redirect, render_template, request
from ft_app.models.dbc.database import db_session

bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("exercises/index.html")
