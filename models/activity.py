"""
Activity log model: raw SQL access to the `activity_logs` table.
Each row is one study session (date + hours), used for weekly/monthly
trend charts, streak calculation, and the Learning Health Score.
"""
from datetime import date
from utils.db import query_all, execute


def log_activity(user_id, course_id, hours_spent, activity_date=None):
    execute(
        """INSERT INTO activity_logs (user_id, course_id, activity_date, hours_spent)
           VALUES (%s, %s, %s, %s)""",
        (user_id, course_id, activity_date or date.today(), hours_spent)
    )


def get_activity(user_id, since=None):
    if since:
        return query_all(
            "SELECT activity_date, hours_spent FROM activity_logs WHERE user_id = %s AND activity_date >= %s",
            (user_id, since)
        )
    return query_all(
        "SELECT activity_date, hours_spent FROM activity_logs WHERE user_id = %s",
        (user_id,)
    )


def distinct_active_dates(user_id):
    rows = query_all(
        "SELECT DISTINCT activity_date FROM activity_logs WHERE user_id = %s ORDER BY activity_date DESC",
        (user_id,)
    )
    return [r["activity_date"] for r in rows]
