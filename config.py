"""
Application configuration.

Reads DB credentials from environment variables when present, and falls back
to sane local-dev defaults so the project runs out-of-the-box with a local
MySQL server. For a real deployment, set these as environment variables
instead of editing this file.
"""
import os


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "learning-path-dashboard-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # MySQL connection settings (used by utils/db.py)
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "4000"))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "learning_path_db")

    # File uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "certificates")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

    # Fixed reference lists used across the app
    SKILL_NAMES = [
        "Python", "Java", "Web Development", "Data Analytics",
        "Machine Learning", "UI/UX", "Cloud Computing", "Cyber Security"
    ]

    CAREER_GOALS = [
        "Data Analyst", "Data Scientist", "Full Stack Developer",
        "Machine Learning Engineer", "Cloud Engineer", "UI/UX Designer",
        "Cyber Security Analyst", "DevOps Engineer"
    ]

    # Learning Health Score weights (must sum to 1.0)
    HEALTH_SCORE_WEIGHTS = {
        "completion": 0.35,   # course completion rate
        "skill": 0.25,        # average self-rated skill level
        "consistency": 0.20,  # study streak / recent activity
        "goals": 0.20,        # goal achievement rate
    }
