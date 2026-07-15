"""
Dashboard route: the main landing page after login.
"""
from flask import Blueprint, render_template, g

from controllers.analytics_controller import dashboard_data
from controllers.learning_path_controller import get_recommendations
from utils.decorators import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def root():
    from flask import redirect, url_for
    if g.user:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.login"))


@bp.route("/dashboard")
@login_required
def dashboard():
    data = dashboard_data(g.user["user_id"])
    recommendations = get_recommendations(g.user["user_id"], g.user["career_goal"], limit=3)
    return render_template("dashboard.html", recommendations=recommendations, **data)
