"""
Progress model: raw SQL access to the `progress` table
(a user's enrollment + completion state in a specific course).
"""
from datetime import datetime
from utils.db import query_all, query_one, execute


def get_user_progress(user_id):
    """All progress rows for a user, joined with course details."""
    sql = """
        SELECT p.*, c.name AS course_name, c.domain, c.duration_hours, c.difficulty
        FROM progress p
        JOIN courses c ON c.course_id = p.course_id
        WHERE p.user_id = %s
    """
    return query_all(sql, (user_id,))


def get_enrollment(user_id, course_id):
    return query_one(
        "SELECT * FROM progress WHERE user_id = %s AND course_id = %s",
        (user_id, course_id)
    )


def enroll(user_id, course_id):
    existing = get_enrollment(user_id, course_id)
    if existing:
        return existing["progress_id"]
    progress_id, _ = execute(
        """INSERT INTO progress (user_id, course_id, status, progress_percent)
           VALUES (%s, %s, 'In Progress', 0)""",
        (user_id, course_id)
    )
    return progress_id


def update_progress(user_id, course_id, progress_percent):
    if progress_percent >= 100:
        status = "Completed"
        sql = """UPDATE progress SET progress_percent = %s, status = %s, completed_at = %s
                  WHERE user_id = %s AND course_id = %s"""
        execute(sql, (progress_percent, status, datetime.utcnow(), user_id, course_id))
    else:
        status = "In Progress" if progress_percent > 0 else "Not Started"
        sql = """UPDATE progress SET progress_percent = %s, status = %s
                  WHERE user_id = %s AND course_id = %s"""
        execute(sql, (progress_percent, status, user_id, course_id))


def completed_course_ids(user_id):
    rows = query_all(
        "SELECT course_id FROM progress WHERE user_id = %s AND status IN ('Completed','In Progress')",
        (user_id,)
    )
    return {r["course_id"] for r in rows}


def summary_counts(user_id):
    sql = """
        SELECT
          COUNT(*) AS total_courses,
          SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
          SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
          SUM(CASE WHEN status = 'Not Started' THEN 1 ELSE 0 END) AS pending,
          COALESCE(SUM(c.duration_hours), 0) AS total_hours
        FROM progress p
        JOIN courses c ON c.course_id = p.course_id
        WHERE p.user_id = %s
    """
    row = query_one(sql, (user_id,))
    return {
        "total_courses": row["total_courses"] or 0,
        "completed": row["completed"] or 0,
        "in_progress": row["in_progress"] or 0,
        "pending": row["pending"] or 0,
        "total_hours": row["total_hours"] or 0,
    }


def domain_hours_completed(user_id):
    sql = """
        SELECT c.domain, SUM(c.duration_hours) AS hours
        FROM progress p
        JOIN courses c ON c.course_id = p.course_id
        WHERE p.user_id = %s AND p.status = 'Completed'
        GROUP BY c.domain
        ORDER BY hours DESC
    """
    return query_all(sql, (user_id,))


def count_all_enrollments():
    row = query_one("SELECT COUNT(*) AS cnt FROM progress")
    return row["cnt"] if row else 0


def count_all_completions():
    row = query_one("SELECT COUNT(*) AS cnt FROM progress WHERE status = 'Completed'")
    return row["cnt"] if row else 0
