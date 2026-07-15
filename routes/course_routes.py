"""
Course catalog, enrollment, and progress-update routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from controllers.course_controller import (
    list_courses, list_domains, enrolled_map, enroll_in_course, record_progress
)
from utils.decorators import login_required

bp = Blueprint("courses", __name__)


@bp.route("/courses")
@login_required
def courses():
    domain_filter = request.args.get("domain", "")
    course_rows = list_courses(domain=domain_filter or None)
    return render_template(
        "courses.html",
        courses=course_rows,
        enrolled=enrolled_map(g.user["user_id"]),
        domains=list_domains(),
        current_domain=domain_filter,
    )


@bp.route("/courses/<int:course_id>/enroll", methods=["POST"])
@login_required
def enroll(course_id):
    enroll_in_course(g.user["user_id"], course_id)
    flash("Enrolled successfully.", "success")
    return redirect(request.referrer or url_for("courses.courses"))


@bp.route("/courses/<int:course_id>/progress", methods=["POST"])
@login_required
def update_progress(course_id):
    try:
        progress_percent = int(request.form.get("progress_percent", 0))
    except (ValueError, TypeError):
        progress_percent = 0
    try:
        hours_spent = float(request.form.get("hours_spent", 1))
    except (ValueError, TypeError):
        hours_spent = 1.0

    record_progress(g.user["user_id"], course_id, progress_percent, hours_spent)
    flash("Progress updated.", "success")
    return redirect(request.referrer or url_for("courses.courses"))
