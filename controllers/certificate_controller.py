"""
Certificate controller: file upload handling + portfolio management.
"""
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from models.certificate import add_certificate, get_certificates, find_certificate, delete_certificate as delete_row


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def upload_certificate(user_id, form, file, upload_folder, allowed_extensions):
    """Returns (success: bool, message: str)."""
    title = form.get("title", "").strip()
    platform = form.get("platform", "").strip()

    if not title:
        return False, "Please provide a certificate title."
    if not file or not file.filename or not allowed_file(file.filename, allowed_extensions):
        return False, "Please upload a valid file (pdf, png, jpg, jpeg)."

    filename = secure_filename(f"{user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}")
    file.save(os.path.join(upload_folder, filename))
    add_certificate(user_id, platform, title, filename)
    return True, "Certificate uploaded."


def list_certificates(user_id):
    return get_certificates(user_id)


def remove_certificate(user_id, cert_id, upload_folder):
    cert = find_certificate(cert_id, user_id)
    if not cert:
        return False
    try:
        os.remove(os.path.join(upload_folder, cert["filename"]))
    except OSError:
        pass
    delete_row(cert_id, user_id)
    return True
