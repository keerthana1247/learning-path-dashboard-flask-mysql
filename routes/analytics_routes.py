"""
Analytics page routes.
"""
from flask import Blueprint, render_template, g

from controllers.analytics_controller import analytics_page_data
from controllers.skill_controller import strongest_weakest
from utils.decorators import login_required

bp = Blueprint("analytics", __name__)


@bp.route("/analytics")
@login_required
def analytics():
    data = analytics_page_data(g.user["user_id"])
    sw = strongest_weakest(g.user["user_id"])
    return render_template("analytics.html", strongest_weakest=sw, **data)
