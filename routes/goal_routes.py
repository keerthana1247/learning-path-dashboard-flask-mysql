"""
Goal tracking routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from controllers.goal_controller import add_goal, list_goals, update_goal, remove_goal
from utils.decorators import login_required

bp = Blueprint("goals", __name__)


@bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    if request.method == "POST":
        if add_goal(g.user["user_id"], request.form):
            flash("Goal created.", "success")
        else:
            flash("Please provide a goal title.", "danger")
        return redirect(url_for("goals.goals"))

    data = list_goals(g.user["user_id"])
    return render_template("goals.html", weekly_goals=data["weekly"], monthly_goals=data["monthly"])


@bp.route("/goals/<int:goal_id>/progress", methods=["POST"])
@login_required
def goal_progress(goal_id):
    try:
        current_value = int(request.form.get("current_value", 0))
    except (ValueError, TypeError):
        current_value = 0
    update_goal(g.user["user_id"], goal_id, current_value)
    flash("Goal progress updated.", "success")
    return redirect(url_for("goals.goals"))


@bp.route("/goals/<int:goal_id>/delete", methods=["POST"])
@login_required
def goal_delete(goal_id):
    remove_goal(g.user["user_id"], goal_id)
    flash("Goal removed.", "info")
    return redirect(url_for("goals.goals"))
