from flask import Blueprint, render_template

bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@bp.route('/', methods=["POST", "GET"])
def index():
    return render_template("exercises/index.html")
