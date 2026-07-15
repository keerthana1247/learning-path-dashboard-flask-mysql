"""
Course model: raw SQL access to the `courses` table.
"""
from utils.db import query_all, query_one, execute


def all_courses(domain=None):
    if domain:
        return query_all(
            "SELECT * FROM courses WHERE domain = %s ORDER BY domain, name",
            (domain,)
        )
    return query_all("SELECT * FROM courses ORDER BY domain, name")


def all_domains():
    rows = query_all("SELECT DISTINCT domain FROM courses ORDER BY domain")
    return [r["domain"] for r in rows]


def find_by_id(course_id):
    return query_one("SELECT * FROM courses WHERE course_id = %s", (course_id,))


def create_course(name, domain, duration_hours, difficulty, description):
    course_id, _ = execute(
        """INSERT INTO courses (name, domain, duration_hours, difficulty, description)
           VALUES (%s, %s, %s, %s, %s)""",
        (name, domain, duration_hours, difficulty, description)
    )
    return course_id


def update_course(course_id, name, domain, duration_hours, difficulty, description):
    execute(
        """UPDATE courses
           SET name = %s, domain = %s, duration_hours = %s,
               difficulty = %s, description = %s
           WHERE course_id = %s""",
        (name, domain, duration_hours, difficulty, description, course_id)
    )


def delete_course(course_id):
    execute("DELETE FROM courses WHERE course_id = %s", (course_id,))


def count_courses():
    row = query_one("SELECT COUNT(*) AS cnt FROM courses")
    return row["cnt"] if row else 0
