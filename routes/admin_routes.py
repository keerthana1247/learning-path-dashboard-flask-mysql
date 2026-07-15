"""
Admin panel routes: learner overview, course catalog management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from controllers.analytics_controller import admin_overview
from models.user import all_learners
from models.course import all_courses, create_course, update_course, delete_course
from utils.decorators import login_required, admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin.html", **admin_overview())


@bp.route("/users")
@login_required
@admin_required
def users():
    return render_template("admin_users.html", users=all_learners())


@bp.route("/courses", methods=["GET", "POST"])
@login_required
@admin_required
def courses():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        domain = request.form.get("domain", "").strip()
        try:
            duration = int(request.form.get("duration_hours", 10))
        except (ValueError, TypeError):
            duration = 10
        difficulty = request.form.get("difficulty", "Beginner")
        description = request.form.get("description", "")

        if name and domain:
            create_course(name, domain, duration, difficulty, description)
            flash("Course added.", "success")
        else:
            flash("Course name and domain are required.", "danger")
        return redirect(url_for("admin.courses"))

    return render_template("admin_courses.html", courses=all_courses())


@bp.route("/courses/<int:course_id>/edit", methods=["POST"])
@login_required
@admin_required
def edit_course(course_id):
    try:
        duration = int(request.form.get("duration_hours", 10))
    except (ValueError, TypeError):
        duration = 10
    update_course(
        course_id,
        request.form.get("name", ""),
        request.form.get("domain", ""),
        duration,
        request.form.get("difficulty", "Beginner"),
        request.form.get("description", ""),
    )
    flash("Course updated.", "success")
    return redirect(url_for("admin.courses"))


@bp.route("/courses/<int:course_id>/delete", methods=["POST"])
@login_required
@admin_required
def remove_course(course_id):
    delete_course(course_id)
    flash("Course deleted.", "info")
    return redirect(url_for("admin.courses"))
