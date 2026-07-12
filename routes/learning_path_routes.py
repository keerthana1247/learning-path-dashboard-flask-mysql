"""
Learning path routes.
"""
from flask import Blueprint, render_template, g

from controllers.learning_path_controller import get_path, get_recommendations
from utils.decorators import login_required

bp = Blueprint("learning_path", __name__)


@bp.route("/learning-path")
@login_required
def learning_path():
    career_goal = g.user["career_goal"]
    path = get_path(g.user["user_id"], career_goal)
    recommendations = get_recommendations(g.user["user_id"], career_goal, limit=5)
    return render_template("learning_path.html", path=path, recommendations=recommendations,
                           career_goal=career_goal)
