from flask import render_template, url_for, session, Blueprint, redirect

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    role = session.get("role", "").lower().strip()

    if role == "owner":
        return render_template("dashboard_owner.html", email=session["email"])

    if role == "petugas":
        return render_template("dashboard_petugas.html", email=session["email"])

    session.clear()
    return redirect("/login")
