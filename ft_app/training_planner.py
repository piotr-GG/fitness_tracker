from flask import Blueprint, flash, redirect, render_template, request
from ft_app.models.dbc.database import db_session

bp = Blueprint("training_planner", __name__, url_prefix="/tp")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("training_planner/index.html")
