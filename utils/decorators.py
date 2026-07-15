"""
Session-based authentication helpers.

The app stores `user_id` and `is_admin` in Flask's signed session cookie on
login. These decorators guard routes that require a logged-in user or an
admin account.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, abort, g, request

from models.user import find_by_id


def load_logged_in_user():
    """Called via app.before_request: attach the current user to `g.user`."""
    if request.endpoint == "static":
        g.user = None
        return
    user_id = session.get("user_id")
    g.user = find_by_id(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            flash("Please log in to access the dashboard.", "info")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None or not g.user.get("is_admin"):
            abort(403)
        return view(*args, **kwargs)
    return wrapped
