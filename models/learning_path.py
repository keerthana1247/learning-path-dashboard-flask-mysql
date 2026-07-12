"""
Learning path model: raw SQL access to the `learning_paths` table
(the ordered course sequence defined for each career goal).
"""
from utils.db import query_all, execute


def steps_for_goal(career_goal):
    """Return ordered path steps joined with course details."""
    sql = """
        SELECT lp.path_id, lp.career_goal, lp.step_order,
               c.course_id, c.name, c.domain, c.duration_hours, c.difficulty
        FROM learning_paths lp
        JOIN courses c ON c.course_id = lp.course_id
        WHERE lp.career_goal = %s
        ORDER BY lp.step_order ASC
    """
    return query_all(sql, (career_goal,))


def add_step(career_goal, course_id, step_order):
    execute(
        "INSERT INTO learning_paths (career_goal, course_id, step_order) VALUES (%s, %s, %s)",
        (career_goal, course_id, step_order)
    )
