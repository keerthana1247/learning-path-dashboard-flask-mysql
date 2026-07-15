# ---------------------------------------------------------------------------
# Learning Path Dashboard — Flask app container
# ---------------------------------------------------------------------------
FROM python:3.11-slim

WORKDIR /app

# System deps needed to build mysql-connector-python / pandas wheels cleanly
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p static/uploads/certificates

ENV FLASK_DEBUG=0
EXPOSE 5000

# Gunicorn serves the `app` object exported from wsgi.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "wsgi:app"]
