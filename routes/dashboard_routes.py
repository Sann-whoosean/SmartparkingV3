from flask import redirect, session, Blueprint, url_for

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/")

    role = session.get("role", "").lower().strip()

    if role == "owner":
        return redirect("/owner")

    if role == "petugas":
        return redirect("/petugas")

    return redirect("/")
