"""
Analytics controller: aggregates data for the dashboard/analytics pages and
the admin panel, and wraps the Plotly chart builders + Learning Health Score.
"""
from datetime import date, timedelta

from models.progress import summary_counts, count_all_enrollments, count_all_completions
from models.goal import get_active_goals
from models.user import count_learners, count_by_career_goal
from models.course import count_courses
from utils import charts
from utils.health_score import calculate_health_score
from config import Config


def dashboard_data(user_id):
    return {
        "summary": summary_counts(user_id),
        "active_goals": get_active_goals(user_id, limit=3),
        "weekly_fig": charts.weekly_hours_figure(user_id),
        "monthly_fig": charts.monthly_hours_figure(user_id),
        "radar_fig": charts.skill_radar_figure(user_id),
        "health": calculate_health_score(user_id, Config.HEALTH_SCORE_WEIGHTS),
    }


def analytics_page_data(user_id):
    health = calculate_health_score(user_id, Config.HEALTH_SCORE_WEIGHTS)
    return {
        "summary": summary_counts(user_id),
        "domain_fig": charts.domain_distribution_figure(user_id),
        "health": health,
        "gauge_fig": charts.health_score_gauge_figure(
            health["score"],
            {"teal": "#4FD1C5", "amber": "#F2A93B", "danger": "#F2666A"}[health["tone"]]
        ),
        "prediction": charts.prediction_trend(user_id),
    }


def admin_overview():
    goal_counts = {goal: count_by_career_goal(goal) for goal in Config.CAREER_GOALS}
    return {
        "total_users": count_learners(),
        "total_courses": count_courses(),
        "total_enrollments": count_all_enrollments(),
        "total_completions": count_all_completions(),
        "goal_counts": goal_counts,
    }
