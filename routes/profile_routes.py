"""
Profile routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from controllers.profile_controller import save_profile
from utils.decorators import login_required
from config import Config

bp = Blueprint("profile", __name__)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        save_profile(g.user["user_id"], request.form)
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile.html", career_goals=Config.CAREER_GOALS)
