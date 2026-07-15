"""
Skill assessment routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from controllers.skill_controller import get_skills_dict, save_skill_ratings
from utils.decorators import login_required
from utils import charts
from config import Config

bp = Blueprint("skills", __name__)


@bp.route("/skills", methods=["GET", "POST"])
@login_required
def skills():
    if request.method == "POST":
        save_skill_ratings(g.user["user_id"], request.form)
        flash("Skill assessment saved.", "success")
        return redirect(url_for("skills.skills"))

    user_skills = get_skills_dict(g.user["user_id"])
    radar_fig = charts.skill_radar_figure(g.user["user_id"])
    return render_template("skills.html", skill_names=Config.SKILL_NAMES,
                           user_skills=user_skills, radar_fig=radar_fig)
