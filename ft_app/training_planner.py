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

    form = ExerciseMainForm()

    if request.method == "POST":
        print("INSIDE POST METHOD!")
        form = ExerciseMainForm(request.form)
        if form.validate():
            print("FORM VALIDATED!")
            data = {}
            for i, exercise_form in enumerate(form.exercises, start=1):
                exercise_id = exercise_form.ex_id.data
                exercise_sets = exercise_form.sets.data
                exercise_name = exercise_form.exercise_name.data
                exercise_repetitions = exercise_form.reps.data
                data[i] = (exercise_id, exercise_name, exercise_sets, exercise_repetitions)
                print(exercise_id, exercise_sets, exercise_repetitions)
        else:
            print("FORM VALIDATION FAILED!")
            print(form.errors)

        return render_template("training_planner/create_modify.html",
                               form=form, data=data)
    else:
        data = {}
        for i, exercise in enumerate(training_plan_unit.exercise_records, start=1):
            ex_rec_form = ExerciseRecordForm()
            ex_rec_form.ex_id.data = exercise.id
            ex_rec_form.exercise_name.data = exercise.exercise.name
            ex_rec_form.sets.data = exercise.sets
            ex_rec_form.reps.data = exercise.repetitions
            data[i] = (exercise.id, exercise.exercise.name, exercise.sets, exercise.repetitions)
            form.exercises.append_entry(ex_rec_form)
        return render_template("training_planner/create_modify.html",
                               form=form, data=data)
