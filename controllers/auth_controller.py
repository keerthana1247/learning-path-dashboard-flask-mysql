"""
Auth controller: business logic for registration, login, and password reset.
Routes call into these functions and just handle the HTTP/session concerns.
"""
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import create_user, find_by_email, update_password
from models.skill import init_skills_for_user
from config import Config


def register_user(name, email, password, confirm_password):
    """Returns (success: bool, message: str)."""
    email = email.strip().lower()
    name = name.strip()

    if not name or not email or not password:
        return False, "Please fill in all required fields."
    if password != confirm_password:
        return False, "Passwords do not match."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if find_by_email(email):
        return False, "An account with that email already exists."

    user_id = create_user(name, email, generate_password_hash(password))
    init_skills_for_user(user_id, Config.SKILL_NAMES)
    return True, "Account created! Please log in."


def authenticate(email, password):
    """Returns the user dict on success, or None on failure."""
    user = find_by_email(email.strip().lower())
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def reset_password(email, new_password):
    """Returns (success: bool, message: str)."""
    user = find_by_email(email.strip().lower())
    if user and new_password and len(new_password) >= 6:
        update_password(user["user_id"], generate_password_hash(new_password))
        return True, "Password reset successful. Please log in."
    return False, "We couldn't reset that password. Check the email and try again."
