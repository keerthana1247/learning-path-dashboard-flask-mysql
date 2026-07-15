"""
Learning Path Dashboard — Flask + MySQL + Plotly

Run with:  python app.py
Then visit http://127.0.0.1:5000

Before first run, create the database and seed reference data:
  mysql -u root -p < database/schema.sql
(the course catalog, learning paths, and default admin account are then
seeded automatically and idempotently by utils/seed.py on every app start)

Default admin login: admin@learnpath.local / admin123
"""
import os
from flask import Flask, g, render_template

from config import Config
from utils import db as db_utils
from utils.decorators import load_logged_in_user
from utils.seed import run_seed

from routes import auth_routes, dashboard_routes, profile_routes, skill_routes
from routes import course_routes, learning_path_routes, goal_routes
from routes import certificate_routes, analytics_routes, admin_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db_utils.init_app(app)

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(profile_routes.bp)
    app.register_blueprint(skill_routes.bp)
    app.register_blueprint(course_routes.bp)
    app.register_blueprint(learning_path_routes.bp)
    app.register_blueprint(goal_routes.bp)
    app.register_blueprint(certificate_routes.bp)
    app.register_blueprint(analytics_routes.bp)
    app.register_blueprint(admin_routes.bp)

    app.before_request(load_logged_in_user)

    @app.context_processor
    def inject_user():
        return {"current_user": g.get("user")}

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403, message="You don't have permission to view this page."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="That page doesn't exist."), 404

    # Seed the course catalog / learning paths / default admin account.
    # Safe to call on every startup — each step is idempotent.
    run_seed(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
