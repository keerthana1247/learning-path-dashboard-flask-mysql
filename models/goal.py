"""
Goal model: raw SQL access to the `goals` table.
"""
from utils.db import query_all, query_one, execute


def create_goal(user_id, title, goal_type, target_value, start_date, end_date):
    goal_id, _ = execute(
        """INSERT INTO goals (user_id, title, goal_type, target_value, current_value, start_date, end_date)
           VALUES (%s, %s, %s, %s, 0, %s, %s)""",
        (user_id, title, goal_type, target_value, start_date, end_date)
    )
    return goal_id


def get_goals(user_id, goal_type=None):
    if goal_type:
        return query_all(
            "SELECT * FROM goals WHERE user_id = %s AND goal_type = %s ORDER BY start_date DESC",
            (user_id, goal_type)
        )
    return query_all("SELECT * FROM goals WHERE user_id = %s ORDER BY start_date DESC", (user_id,))


def get_active_goals(user_id, limit=3):
    return query_all(
        "SELECT * FROM goals WHERE user_id = %s AND completed = FALSE ORDER BY start_date DESC LIMIT %s",
        (user_id, limit)
    )


def find_goal(goal_id, user_id):
    return query_one("SELECT * FROM goals WHERE goal_id = %s AND user_id = %s", (goal_id, user_id))


def update_progress(goal_id, current_value, completed):
    execute(
        "UPDATE goals SET current_value = %s, completed = %s WHERE goal_id = %s",
        (current_value, completed, goal_id)
    )


def delete_goal(goal_id, user_id):
    execute("DELETE FROM goals WHERE goal_id = %s AND user_id = %s", (goal_id, user_id))


def completion_rate(user_id):
    row = query_one(
        """SELECT COUNT(*) AS total, SUM(CASE WHEN completed THEN 1 ELSE 0 END) AS done
           FROM goals WHERE user_id = %s""",
        (user_id,)
    )
    total = row["total"] or 0
    done = row["done"] or 0
    return (done / total * 100) if total else 0
