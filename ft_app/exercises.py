from flask import Blueprint, render_template, request

from ft_app.dbc.queries import get_exercises

bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return render_template("exercises/index.html")
    else:
        exercises = get_exercises()
        return render_template("exercises/index.html", exercises=exercises)

