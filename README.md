# Learning Path Dashboard for Enhancing Skills Using Python with Data Analytics

A full-stack Flask + MySQL + Plotly web application that gives learners a personalized skill-development dashboard: skill assessments, career-goal-based learning paths, course/progress tracking, a computed **Learning Health Score**, analytics, goal tracking, and a certificate portfolio — plus an admin panel.

**Tech stack (matches project report):**
- **Backend:** Python, Flask
- **Database:** MySQL
- **Visualization:** Plotly (server-generated figures rendered client-side with Plotly.js)
- **Frontend:** HTML5, CSS3, Bootstrap, JavaScript (Jinja2 templates)

---

## 1. Folder structure

```
lpd_mysql/
├── app.py                     # Application factory — registers all blueprints
├── config.py                  # Flask + MySQL configuration, constants, HLS weights
├── requirements.txt
├── database/
│   ├── schema.sql              # CREATE DATABASE + all CREATE TABLE statements
│   └── seed_data.sql           # Reference SQL for course catalog + learning paths
├── models/                     # Data-access layer (raw SQL via mysql-connector)
│   ├── user.py
│   ├── skill.py
│   ├── course.py
│   ├── learning_path.py
│   ├── progress.py
│   ├── activity.py
│   ├── goal.py
│   └── certificate.py
├── controllers/                # Business logic layer (called by routes)
│   ├── auth_controller.py
│   ├── profile_controller.py
│   ├── skill_controller.py
│   ├── course_controller.py
│   ├── learning_path_controller.py
│   ├── goal_controller.py
│   ├── certificate_controller.py
│   └── analytics_controller.py
├── routes/                     # Flask Blueprints (HTTP layer only)
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── profile_routes.py
│   ├── skill_routes.py
│   ├── course_routes.py
│   ├── learning_path_routes.py
│   ├── goal_routes.py
│   ├── certificate_routes.py
│   ├── analytics_routes.py
│   └── admin_routes.py
├── utils/
│   ├── db.py                   # MySQL connection pool + query helpers
│   ├── decorators.py           # login_required / admin_required (session-based)
│   ├── charts.py               # Plotly figure builders (pandas + NumPy analytics)
│   ├── health_score.py         # Learning Health Score calculation
│   ├── recommendations.py      # Personalized course recommendation engine
│   └── seed.py                 # Idempotent startup seeding (catalog + admin user)
├── templates/                  # Jinja2 + Bootstrap frontend
│   ├── base.html                # Shared app shell (sidebar nav, flash messages)
│   ├── login.html / register.html / forgot_password.html
│   ├── dashboard.html / skills.html / learning_path.html / courses.html
│   ├── analytics.html / goals.html / certificates.html / profile.html
│   ├── admin.html / admin_users.html / admin_courses.html
│   └── error.html
└── static/
    ├── css/style.css           # Design system
    └── uploads/certificates/   # Uploaded certificate files
```

**Architecture flow:** `routes/` (HTTP request/response only) → `controllers/` (business logic, validation) → `models/` (raw SQL against MySQL) → back up through the same chain, with `utils/charts.py` and `utils/health_score.py` feeding analytics into the controllers.

---

## 2. Database design

| Table | Purpose |
|---|---|
| `users` | Accounts: name, email, password hash, profile fields, career goal, admin flag |
| `skills` | Per-user self-rated proficiency (0–100) in each tracked skill |
| `courses` | Master course catalog (name, domain, duration, difficulty, description) |
| `learning_paths` | Ordered course sequence for each career goal |
| `progress` | A user's enrollment + completion % in a course |
| `activity_logs` | Daily study-hour entries — powers charts, streaks, and the Health Score |
| `goals` | Weekly/monthly targets with current/target progress |
| `certificates` | Uploaded certificate metadata + filename |

Full `CREATE TABLE` statements with constraints, foreign keys, and indexes are in **`database/schema.sql`**.

### Entity relationships
- `users (1) → (many) skills, progress, goals, certificates, activity_logs`
- `courses (1) → (many) progress, activity_logs, learning_paths`
- `learning_paths` links a `career_goal` string to an ordered list of `courses`

---

## 3. Installation

### Prerequisites
- Python 3.10+
- MySQL Server 8.0+ (or MariaDB 10.5+) running locally or reachable over network

### Step 1 — Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### Step 2 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Create the MySQL database and tables
```bash
mysql -u root -p < database/schema.sql
```
This creates the `learning_path_db` database and all required tables.

*(Optional)* Load the reference seed SQL manually:
```bash
mysql -u root -p learning_path_db < database/seed_data.sql
```
> You can skip this — `app.py` seeds the course catalog, learning paths, and a default admin account automatically and idempotently on first run via `utils/seed.py`, using a properly generated password hash.

### Step 4 — Configure your MySQL credentials
Set environment variables (recommended) or edit the defaults in `config.py`:
```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_mysql_password
export MYSQL_DATABASE=learning_path_db
export SECRET_KEY=some-random-secret-key
```
On Windows (PowerShell): `$env:MYSQL_PASSWORD="your_mysql_password"`

---

## 4. Running the project

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

- **Create your own account** via "Create an account" on the login page, then set a career goal in **Profile** to unlock personalized recommendations.
- **Admin demo account** (seeded automatically):
  - Email: `admin@learnpath.local`
  - Password: `admin123`

---

## 5. Feature summary

| Feature | Where it lives |
|---|---|
| Registration / login / logout / password reset | `routes/auth_routes.py`, `controllers/auth_controller.py` |
| Profile management | `routes/profile_routes.py` |
| Skill tracking + radar chart | `routes/skill_routes.py`, `utils/charts.py::skill_radar_figure` |
| Learning path management | `routes/learning_path_routes.py`, `utils/recommendations.py` |
| Course management + enrollment/progress | `routes/course_routes.py`, `routes/admin_routes.py` (catalog CRUD) |
| Goal tracking (weekly/monthly) | `routes/goal_routes.py` |
| Certificate management (upload/view/delete) | `routes/certificate_routes.py` |
| Progress analytics (weekly/monthly hours, domain split) | `routes/analytics_routes.py`, `utils/charts.py` |
| **Learning Health Score** | `utils/health_score.py` — weighted blend of completion rate, average skill level, study-streak consistency, and goal-achievement rate (weights configurable in `config.py`) |
| Personalized recommendations | `utils/recommendations.py::recommend_courses` — walks the ordered `learning_paths` sequence for the learner's career goal, skipping courses already started/completed |
| Admin panel | `routes/admin_routes.py` — learner list, course CRUD, aggregate analytics |

---

## 6. How to run — quick checklist

1. `mysql -u root -p < database/schema.sql`
2. `pip install -r requirements.txt`
3. `python app.py`
4. Visit `http://127.0.0.1:5000`

---

## 7. Uploading to GitHub

```bash
# 1. Initialize git in the project folder
cd lpd_mysql
git init

# 2. Add a .gitignore (already included) so venv/, __pycache__/, and
#    uploaded certificate files aren't committed
git add .
git commit -m "Initial commit: Learning Path Dashboard (Flask + MySQL + Plotly)"

# 3. Create a new empty repository on GitHub (via the website), then:
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

**Before pushing**, double-check that:
- `.gitignore` excludes `venv/`, `__pycache__/`, `static/uploads/certificates/*`, and any `.env` file with real credentials
- You have **not** hard-coded your real MySQL password in `config.py` — use environment variables instead
- Add a short note in your GitHub repo description pointing to this README for setup steps

---

## 8. Customizing

- **Add/modify courses or learning paths:** edit `utils/seed.py` (applied only when the `courses` table is empty), or use the running app's **Admin Panel** to add/edit/delete courses live.
- **Add a new career goal:** add it to `Config.CAREER_GOALS` in `config.py` and add a matching entry to `LEARNING_PATHS` in `utils/seed.py`.
- **Tune the Learning Health Score weights:** edit `Config.HEALTH_SCORE_WEIGHTS` in `config.py` (must sum to 1.0).
- **Styling:** design tokens (colors, fonts, spacing) are CSS custom properties at the top of `static/css/style.css`.

## 9. Resetting the database

```sql
DROP DATABASE learning_path_db;
```
then re-run `mysql -u root -p < database/schema.sql` and restart the app — the catalog and admin account will be reseeded automatically.
