"""
Personalized learning recommendations.

Primary strategy: walk the ordered `learning_paths` sequence for the user's
chosen career goal and return the next steps they haven't started/completed.

Secondary strategy (used when a goal isn't set, or to enrich the "why"): bias
towards courses in the learner's weakest self-rated skill domain.
"""
from models.learning_path import steps_for_goal
from models.progress import completed_course_ids
from models.course import all_courses
from models.skill import get_user_skills


def recommend_courses(user_id, career_goal, limit=5):
    """Next steps in the user's career-goal path, skipping active/completed courses."""
    if not career_goal:
        return []

    steps = steps_for_goal(career_goal)
    taken = completed_course_ids(user_id)

    recs = []
    for step in steps:
        if step["course_id"] in taken:
            continue
        recs.append(step)
        if len(recs) >= limit:
            break
    return recs


def full_path_with_status(user_id, career_goal):
    """The entire ordered path for a goal, annotated with each step's progress."""
    from models.progress import get_user_progress

    if not career_goal:
        return []

    steps = steps_for_goal(career_goal)
    progress_by_course = {p["course_id"]: p for p in get_user_progress(user_id)}

    path = []
    for step in steps:
        p = progress_by_course.get(step["course_id"])
        path.append({
            **step,
            "status": p["status"] if p else "Not Started",
            "progress_percent": p["progress_percent"] if p else 0,
        })
    return path


def weakest_skill_course_suggestions(user_id, limit=3):
    """Suggest beginner courses in the learner's lowest-rated skill domain."""
    skills = get_user_skills(user_id)
    if not skills:
        return []

    weakest = min(skills, key=lambda s: s["rating"])
    domain = weakest["skill_name"]

    matches = [c for c in all_courses(domain=None) if c["domain"] == domain]
    matches.sort(key=lambda c: {"Beginner": 0, "Intermediate": 1, "Advanced": 2}.get(c["difficulty"], 1))
    return matches[:limit]
