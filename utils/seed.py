"""
Idempotent seed routine, run once at app startup (see app.py).

Safe to run every time the app boots: each step checks whether data already
exists before inserting, so restarting the app never creates duplicates.
"""
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

from utils.db import query_one, execute
from models import user as user_model
from models import course as course_model
from models.learning_path import add_step
from models.skill import init_skills_for_user
from config import Config

COURSE_CATALOG = [
    ("Python Basics", "Python", 12, "Beginner", "Core Python syntax, data types, and control flow."),
    ("SQL Fundamentals", "Data Analytics", 10, "Beginner", "Querying relational databases with SQL."),
    ("Statistics for Data Analysis", "Data Analytics", 14, "Beginner", "Descriptive and inferential statistics."),
    ("Excel for Data Analysis", "Data Analytics", 8, "Beginner", "Pivot tables, formulas, and dashboards in Excel."),
    ("Data Visualization Principles", "Data Analytics", 10, "Intermediate", "Designing clear, honest visual stories."),
    ("Pandas for Data Analysis", "Data Analytics", 12, "Intermediate", "Data wrangling with the pandas library."),
    ("NumPy Essentials", "Data Analytics", 8, "Intermediate", "Numerical computing with NumPy arrays."),
    ("Machine Learning Basics", "Machine Learning", 20, "Intermediate", "Supervised/unsupervised learning fundamentals."),
    ("Power BI for Analysts", "Data Analytics", 10, "Intermediate", "Building interactive BI reports and dashboards."),
    ("Portfolio Projects: Data Analytics", "Data Analytics", 15, "Advanced", "Capstone projects for your portfolio."),
    ("Advanced Python", "Python", 14, "Intermediate", "OOP, decorators, generators, and testing."),
    ("Deep Learning Foundations", "Machine Learning", 22, "Advanced", "Neural networks, CNNs, and RNNs."),
    ("Feature Engineering", "Machine Learning", 12, "Intermediate", "Preparing data for predictive models."),
    ("MLOps Fundamentals", "Machine Learning", 14, "Advanced", "Deploying and monitoring ML models."),
    ("Portfolio Projects: Data Science", "Machine Learning", 18, "Advanced", "End-to-end data science capstone."),
    ("HTML, CSS & Bootstrap", "Web Development", 10, "Beginner", "Building responsive page layouts."),
    ("JavaScript Essentials", "Web Development", 14, "Beginner", "Core JS, DOM manipulation, events."),
    ("Flask Web Development", "Web Development", 16, "Intermediate", "Building server-rendered apps with Flask."),
    ("React Fundamentals", "Web Development", 16, "Intermediate", "Component-based front-end development."),
    ("REST API Design", "Web Development", 10, "Intermediate", "Designing and consuming REST APIs."),
    ("Databases for Web Apps", "Web Development", 10, "Intermediate", "Relational modelling with MySQL."),
    ("Portfolio Projects: Full Stack", "Web Development", 20, "Advanced", "A complete full-stack capstone app."),
    ("Cloud Computing Basics", "Cloud Computing", 10, "Beginner", "Core cloud concepts: IaaS, PaaS, SaaS."),
    ("AWS Fundamentals", "Cloud Computing", 16, "Intermediate", "Core AWS services: EC2, S3, IAM."),
    ("Docker & Containers", "Cloud Computing", 12, "Intermediate", "Containerizing and shipping applications."),
    ("Kubernetes Essentials", "Cloud Computing", 16, "Advanced", "Orchestrating containers at scale."),
    ("CI/CD Pipelines", "Cloud Computing", 12, "Advanced", "Automating build, test, and deploy."),
    ("UI/UX Design Principles", "UI/UX", 10, "Beginner", "Usability heuristics and design thinking."),
    ("Wireframing & Prototyping", "UI/UX", 10, "Beginner", "Low- and high-fidelity prototypes."),
    ("Figma Essentials", "UI/UX", 8, "Beginner", "Designing interfaces in Figma."),
    ("User Research Methods", "UI/UX", 10, "Intermediate", "Interviews, surveys, and usability testing."),
    ("Portfolio Projects: UI/UX", "UI/UX", 14, "Advanced", "A polished case-study portfolio."),
    ("Cyber Security Fundamentals", "Cyber Security", 12, "Beginner", "CIA triad, threats, and vulnerabilities."),
    ("Network Security", "Cyber Security", 14, "Intermediate", "Firewalls, VPNs, and secure protocols."),
    ("Ethical Hacking Basics", "Cyber Security", 16, "Intermediate", "Penetration testing fundamentals."),
    ("Security Operations (SOC)", "Cyber Security", 14, "Advanced", "Incident detection and response."),
    ("Portfolio Projects: Cyber Security", "Cyber Security", 16, "Advanced", "Applied security capstone project."),
    ("Linux & Shell Scripting", "Cloud Computing", 10, "Beginner", "Command-line proficiency and automation."),
    ("Git & Version Control", "Web Development", 6, "Beginner", "Branching, merging, and collaboration."),
]

LEARNING_PATHS = {
    "Data Analyst": [
        "Python Basics", "SQL Fundamentals", "Statistics for Data Analysis",
        "Excel for Data Analysis", "Data Visualization Principles",
        "Pandas for Data Analysis", "NumPy Essentials", "Machine Learning Basics",
        "Power BI for Analysts", "Portfolio Projects: Data Analytics",
    ],
    "Data Scientist": [
        "Python Basics", "Statistics for Data Analysis", "Pandas for Data Analysis",
        "NumPy Essentials", "Machine Learning Basics", "Feature Engineering",
        "Deep Learning Foundations", "MLOps Fundamentals", "Portfolio Projects: Data Science",
    ],
    "Full Stack Developer": [
        "HTML, CSS & Bootstrap", "JavaScript Essentials", "Git & Version Control",
        "Python Basics", "Flask Web Development", "Databases for Web Apps",
        "REST API Design", "React Fundamentals", "Portfolio Projects: Full Stack",
    ],
    "Machine Learning Engineer": [
        "Python Basics", "Advanced Python", "Statistics for Data Analysis",
        "NumPy Essentials", "Machine Learning Basics", "Feature Engineering",
        "Deep Learning Foundations", "MLOps Fundamentals", "Portfolio Projects: Data Science",
    ],
    "Cloud Engineer": [
        "Linux & Shell Scripting", "Cloud Computing Basics", "AWS Fundamentals",
        "Docker & Containers", "Kubernetes Essentials", "CI/CD Pipelines",
    ],
    "UI/UX Designer": [
        "UI/UX Design Principles", "Wireframing & Prototyping", "Figma Essentials",
        "User Research Methods", "HTML, CSS & Bootstrap", "Portfolio Projects: UI/UX",
    ],
    "Cyber Security Analyst": [
        "Cyber Security Fundamentals", "Linux & Shell Scripting", "Network Security",
        "Ethical Hacking Basics", "Security Operations (SOC)", "Portfolio Projects: Cyber Security",
    ],
    "DevOps Engineer": [
        "Linux & Shell Scripting", "Git & Version Control", "Cloud Computing Basics",
        "Docker & Containers", "Kubernetes Essentials", "CI/CD Pipelines",
    ],
}


def run_seed(app):
    with app.app_context():
        if course_model.count_courses() == 0:
            name_to_id = {}
            for name, domain, duration, difficulty, desc in COURSE_CATALOG:
                cid = course_model.create_course(name, domain, duration, difficulty, desc)
                name_to_id[name] = cid

            for goal, course_names in LEARNING_PATHS.items():
                for i, cname in enumerate(course_names, start=1):
                    if cname in name_to_id:
                        add_step(goal, name_to_id[cname], i)

        if not user_model.any_admin_exists():
            admin_id = user_model.create_user(
                "Admin", "admin@learnpath.local", generate_password_hash("admin123")
            )
            execute("UPDATE users SET is_admin = TRUE, career_goal = %s WHERE user_id = %s",
                    ("Data Analyst", admin_id))
            init_skills_for_user(admin_id, Config.SKILL_NAMES)
