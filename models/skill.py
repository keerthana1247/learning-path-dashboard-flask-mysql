"""
Skill model: raw SQL access to the `skills` table.
"""
from utils.db import query_all, execute


def get_user_skills(user_id):
    """Returns a list of dicts: [{skill_name, rating}, ...]"""
    return query_all(
        "SELECT skill_name, rating FROM skills WHERE user_id = %s",
        (user_id,)
    )


def init_skills_for_user(user_id, skill_names):
    """Create zero-rated rows for every tracked skill (called on registration)."""
    for name in skill_names:
        execute(
            """INSERT INTO skills (user_id, skill_name, rating)
               VALUES (%s, %s, 0)
               ON DUPLICATE KEY UPDATE skill_name = skill_name""",
            (user_id, name)
        )


def upsert_skill_rating(user_id, skill_name, rating):
    execute(
        """INSERT INTO skills (user_id, skill_name, rating)
           VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE rating = VALUES(rating)""",
        (user_id, skill_name, rating)
    )
