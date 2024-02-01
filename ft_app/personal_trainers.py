from flask import Blueprint, flash, redirect, render_template, request
from ft_app.models.dbc.database import db_session

bp = Blueprint("personal_trainers", __name__, url_prefix="/pts")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("personal_trainers/index.html")
