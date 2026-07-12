"""
Learning Health Score.

A single 0-100 composite metric summarizing how well a learner is doing,
blending four signals:

  - completion   : % of enrolled courses completed
  - skill        : average self-rated skill level (0-100)
  - consistency  : recent study streak, normalized against a 14-day target
  - goals        : % of set goals achieved

Weights are configured in config.py (Config.HEALTH_SCORE_WEIGHTS) so they can
be tuned without touching the calculation logic.
"""
from datetime import date, timedelta

from models.progress import summary_counts
from models.skill import get_user_skills
from models.goal import completion_rate as goal_completion_rate
from models.activity import distinct_active_dates


def _streak_days(user_id):
    active_days = set(distinct_active_dates(user_id))
    streak = 0
    cursor = date.today()
    while cursor in active_days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def calculate_health_score(user_id, weights):
    summary = summary_counts(user_id)
    total = summary["total_courses"]
    completion_pct = (summary["completed"] / total * 100) if total else 0

    skills = get_user_skills(user_id)
    avg_skill = (sum(s["rating"] for s in skills) / len(skills)) if skills else 0

    streak = _streak_days(user_id)
    consistency_pct = min(streak / 14 * 100, 100)  # 14-day streak = full marks

    goals_pct = goal_completion_rate(user_id)

    score = (
        completion_pct * weights["completion"]
        + avg_skill * weights["skill"]
        + consistency_pct * weights["consistency"]
        + goals_pct * weights["goals"]
    )
    score = round(score, 1)

    if score >= 80:
        label, tone = "Excellent", "teal"
    elif score >= 60:
        label, tone = "Good", "amber"
    elif score >= 40:
        label, tone = "Fair", "amber"
    else:
        label, tone = "Needs Attention", "danger"

    return {
        "score": score,
        "label": label,
        "tone": tone,
        "breakdown": {
            "completion": round(completion_pct, 1),
            "skill": round(avg_skill, 1),
            "consistency": round(consistency_pct, 1),
            "goals": round(goals_pct, 1),
        },
        "streak_days": streak,
    }
