"""
Certificate upload / portfolio routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app

from controllers.certificate_controller import upload_certificate, list_certificates, remove_certificate
from utils.decorators import login_required

bp = Blueprint("certificates", __name__)


@bp.route("/certificates", methods=["GET", "POST"])
@login_required
def certificates():
    if request.method == "POST":
        success, message = upload_certificate(
            g.user["user_id"], request.form, request.files.get("certificate_file"),
            current_app.config["UPLOAD_FOLDER"], current_app.config["ALLOWED_EXTENSIONS"]
        )
        flash(message, "success" if success else "danger")
        return redirect(url_for("certificates.certificates"))

    return render_template("certificates.html", certificates=list_certificates(g.user["user_id"]))


@bp.route("/certificates/<int:cert_id>/delete", methods=["POST"])
@login_required
def delete_certificate(cert_id):
    remove_certificate(g.user["user_id"], cert_id, current_app.config["UPLOAD_FOLDER"])
    flash("Certificate removed.", "info")
    return redirect(url_for("certificates.certificates"))
