"""
MySQL connection handling.

Uses mysql-connector-python with a small connection pool so each request can
grab a connection cheaply. All query helpers return plain dicts (via
dictionary=True cursors) so route/controller code never touches raw tuples.
"""
import mysql.connector
from mysql.connector import pooling
from flask import current_app, g

_pool = None


def init_pool(app):
    """Create the connection pool once, using the app's config."""
    global _pool
    _pool = pooling.MySQLConnectionPool(
        pool_name="lpd_pool",
        pool_size=5,
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
        ssl_ca="ca.pem",
        ssl_verify_cert=True,
        autocommit=False,
    )


def get_db():
    """Return a request-scoped MySQL connection (created lazily, reused per request)."""
    if "db_conn" not in g:
        g.db_conn = _pool.get_connection()
    return g.db_conn


def close_db(e=None):
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()


def init_app(app):
    init_pool(app)
    app.teardown_appcontext(close_db)


# ----------------------------------------------------------------------------
# Query helpers
# ----------------------------------------------------------------------------

def query_all(sql, params=None):
    """Run a SELECT and return a list of dict rows."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cursor.close()
    return rows


def query_one(sql, params=None):
    """Run a SELECT and return a single dict row (or None)."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    row = cursor.fetchone()
    cursor.close()
    return row


def execute(sql, params=None):
    """Run an INSERT/UPDATE/DELETE, commit, and return (lastrowid, rowcount)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    conn.commit()
    last_id, row_count = cursor.lastrowid, cursor.rowcount
    cursor.close()
    return last_id, row_count


def execute_many(sql, seq_of_params):
    """Bulk INSERT/UPDATE using executemany, then commit."""
    if not seq_of_params:
        return 0
    conn = get_db()
    cursor = conn.cursor()
    cursor.executemany(sql, seq_of_params)
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    return row_count


