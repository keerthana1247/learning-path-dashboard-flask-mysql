"""
User model: raw SQL access to the `users` table.
"""
from utils.db import query_one, query_all, execute


def create_user(name, email, password_hash):
    sql = """INSERT INTO users (name, email, password_hash)
             VALUES (%s, %s, %s)"""
    user_id, _ = execute(sql, (name, email, password_hash))
    return user_id


def find_by_email(email):
    return query_one("SELECT * FROM users WHERE email = %s", (email,))


def find_by_id(user_id):
    return query_one("SELECT * FROM users WHERE user_id = %s", (user_id,))


def update_password(user_id, password_hash):
    execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (password_hash, user_id))


def update_profile(user_id, name, college, department, year, career_goal, interests):
    sql = """UPDATE users
             SET name = %s, college = %s, department = %s, year = %s,
                 career_goal = %s, interests = %s
             WHERE user_id = %s"""
    execute(sql, (name, college, department, year, career_goal, interests, user_id))


def all_learners():
    return query_all("""SELECT * FROM users WHERE is_admin = FALSE ORDER BY created_at DESC""")


def count_learners():
    row = query_one("SELECT COUNT(*) AS cnt FROM users WHERE is_admin = FALSE")
    return row["cnt"] if row else 0


def count_by_career_goal(goal):
    row = query_one("SELECT COUNT(*) AS cnt FROM users WHERE career_goal = %s", (goal,))
    return row["cnt"] if row else 0


def any_admin_exists():
    row = query_one("SELECT user_id FROM users WHERE is_admin = TRUE LIMIT 1")
    return row is not None
