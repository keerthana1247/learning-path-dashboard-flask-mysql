"""
WSGI entry point used by production servers (Gunicorn, uWSGI, Render,
Railway, PythonAnywhere, etc.). Points to the same `app` object app.py
creates — this file just avoids running the `if __name__ == "__main__"`
dev-server block.

Example (Gunicorn):
    gunicorn --bind 0.0.0.0:5000 wsgi:app
"""
from app import app

if __name__ == "__main__":
    app.run()
