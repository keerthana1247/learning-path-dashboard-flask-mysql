"""
Certificate model: raw SQL access to the `certificates` table.
"""
from utils.db import query_all, query_one, execute


def add_certificate(user_id, platform, title, filename):
    cert_id, _ = execute(
        """INSERT INTO certificates (user_id, platform, title, filename)
           VALUES (%s, %s, %s, %s)""",
        (user_id, platform, title, filename)
    )
    return cert_id


def get_certificates(user_id):
    return query_all(
        "SELECT * FROM certificates WHERE user_id = %s ORDER BY uploaded_at DESC",
        (user_id,)
    )


def find_certificate(cert_id, user_id):
    return query_one(
        "SELECT * FROM certificates WHERE certificate_id = %s AND user_id = %s",
        (cert_id, user_id)
    )


def delete_certificate(cert_id, user_id):
    execute("DELETE FROM certificates WHERE certificate_id = %s AND user_id = %s", (cert_id, user_id))
