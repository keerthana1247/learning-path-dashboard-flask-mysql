"""
Goal controller: weekly/monthly goal creation and progress tracking.
"""
from datetime import date, timedelta

from models.goal import (
    create_goal, get_goals, find_goal, update_progress as update_goal_row, delete_goal as delete_goal_row
)


def add_goal(user_id, form):
    title = form.get("title", "").strip()
    goal_type = form.get("goal_type", "weekly")
    try:
        target_value = max(1, int(form.get("target_value", 1)))
    except (ValueError, TypeError):
        target_value = 1

    if not title:
        return False

    days = 7 if goal_type == "weekly" else 30
    create_goal(user_id, title, goal_type, target_value, date.today(), date.today() + timedelta(days=days))
    return True


def list_goals(user_id):
    return {
        "weekly": get_goals(user_id, goal_type="weekly"),
        "monthly": get_goals(user_id, goal_type="monthly"),
    }


def update_goal(user_id, goal_id, current_value):
    goal = find_goal(goal_id, user_id)
    if not goal:
        return False
    current_value = max(0, current_value)
    completed = current_value >= goal["target_value"]
    update_goal_row(goal_id, current_value, completed)
    return True


def remove_goal(user_id, goal_id):
    delete_goal_row(goal_id, user_id)
