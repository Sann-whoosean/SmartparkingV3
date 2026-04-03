from flask import url_for, session, Blueprint, redirect

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    role = session.get("role", "").lower().strip()

    if role == "owner":
        return redirect(url_for("owner.owner"))  # Sesuaikan nama fungsi di owner_bp

    if role == "petugas":
        return redirect(url_for("petugas.petugas"))

    session.clear()
    return redirect(url_for("auth.login"))
