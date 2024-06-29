from flask import Blueprint, render_template, g, redirect, url_for, flash, request

from ft_app.auth import login_required
from ft_app.dbc.queries import get_training_plan_for_user, get_training_plan_unit_by_id
from ft_app.forms import ExerciseRecordForm, ExerciseMainForm

bp = Blueprint("training_planner", __name__, url_prefix="/tp")


@login_required
@bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        pass
    else:
        if g.user:
            training_plan = get_training_plan_for_user(g.user.id)
            return render_template("training_planner/index.html",
                                   training_plan=training_plan)
        else:
            flash("You need to be logged in in order to use TrainingPlanner")
            return redirect(url_for("auth.login"))


@login_required
@bp.route('/create_plan', methods=["POST", "GET"])
def create():
    return render_template("training_planner/create_plan.html")


@login_required
@bp.route('/create_unit', methods=["POST", "GET"])
def create_unit():
    return render_template("training_planner/create_unit.html")


@login_required
@bp.route('/modify/<int:tp_unit_id>', methods=["POST", "GET"])
def modify(tp_unit_id):
    training_plan_unit = get_training_plan_unit_by_id(tp_unit_id)
    exercises_form_list = []
    form = ExerciseMainForm(request.form)

    if request.method == "POST":
        if form.validate():
            for i in request.form.items():
                print(i)
        else:
            print(form.errors)
        # print(request.form.items())
        return render_template("training_planner/create_modify.html",
                               form=None)
    else:
        for exercise in training_plan_unit.exercise_records:
            ex_rec_form = ExerciseRecordForm()
            ex_rec_form.ex_id.data = exercise.id
            ex_rec_form.name.data = exercise.exercise.name
            ex_rec_form.sets.data = exercise.sets
            ex_rec_form.reps.data = exercise.repetitions

            exercises_form_list.append(
                ex_rec_form
            )

        form.exercises = exercises_form_list
        return render_template("training_planner/create_modify.html",
                               form=form)
