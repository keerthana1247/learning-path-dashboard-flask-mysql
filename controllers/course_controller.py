"""
Course controller: catalog browsing, enrollment, and progress updates.
"""
from datetime import date

from models.course import all_courses, all_domains
from models.progress import get_user_progress, enroll as enroll_row, update_progress as update_progress_row
from models.activity import log_activity


def list_courses(domain=None):
    return all_courses(domain=domain)


def list_domains():
    return all_domains()


def enrolled_map(user_id):
    """course_id -> progress row, for quick lookup while rendering the catalog."""
    return {p["course_id"]: p for p in get_user_progress(user_id)}


def enroll_in_course(user_id, course_id):
    enroll_row(user_id, course_id)


def record_progress(user_id, course_id, progress_percent, hours_spent):
    progress_percent = max(0, min(100, progress_percent))
    update_progress_row(user_id, course_id, progress_percent)
    log_activity(user_id, course_id, hours_spent, activity_date=date.today())
