"""
Profile controller: read/update a learner's profile fields.
"""
from models.user import update_profile as update_profile_row


def save_profile(user_id, form):
    update_profile_row(
        user_id,
        name=form.get("name", "").strip(),
        college=form.get("college", "").strip(),
        department=form.get("department", "").strip(),
        year=form.get("year", "").strip(),
        career_goal=form.get("career_goal", "").strip(),
        interests=form.get("interests", "").strip(),
    )
