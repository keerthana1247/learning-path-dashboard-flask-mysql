"""
Learning path controller: the recommended course sequence for a career goal.
"""
from utils.recommendations import recommend_courses, full_path_with_status


def get_path(user_id, career_goal):
    return full_path_with_status(user_id, career_goal)


def get_recommendations(user_id, career_goal, limit=5):
    return recommend_courses(user_id, career_goal, limit=limit)
