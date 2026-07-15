"""
Auth routes: registration, login, logout, forgot-password.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g

from controllers.auth_controller import register_user, authenticate, reset_password
from config import Config

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        success, message = register_user(
            request.form.get("name", ""),
            request.form.get("email", ""),
            request.form.get("password", ""),
            request.form.get("confirm_password", ""),
        )
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("auth.login"))

    return render_template("register.html", career_goals=Config.CAREER_GOALS)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        user = authenticate(request.form.get("email", ""), request.form.get("password", ""))
        if user:
            session.clear()
            session["user_id"] = user["user_id"]
            session["is_admin"] = user["is_admin"]
            flash(f"Welcome back, {user['name'].split()[0]}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.dashboard"))
        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        success, message = reset_password(
            request.form.get("email", ""),
            request.form.get("new_password", ""),
        )
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
