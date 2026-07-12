"""
Skill controller: read/save a learner's self-rated skill levels.
"""
from models.skill import get_user_skills, upsert_skill_rating
from config import Config


def get_skills_dict(user_id):
    rows = get_user_skills(user_id)
    return {r["skill_name"]: r["rating"] for r in rows}


def field_name_for(skill_name):
    return f"rating_{skill_name.replace(' ', '_').replace('/', '_')}"


def save_skill_ratings(user_id, form):
    for skill_name in Config.SKILL_NAMES:
        field = field_name_for(skill_name)
        raw_value = form.get(field, 0)
        try:
            value = max(0, min(100, int(raw_value)))
        except (ValueError, TypeError):
            value = 0
        upsert_skill_rating(user_id, skill_name, value)


def strongest_weakest(user_id):
    rows = get_user_skills(user_id)
    if not rows:
        return {"strongest": None, "weakest": None}
    strongest = max(rows, key=lambda r: r["rating"])
    weakest = min(rows, key=lambda r: r["rating"])
    return {
        "strongest": {"name": strongest["skill_name"], "rating": strongest["rating"]},
        "weakest": {"name": weakest["skill_name"], "rating": weakest["rating"]},
    }
