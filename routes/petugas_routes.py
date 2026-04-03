from flask import Blueprint, render_template, redirect, session, jsonify
from config.db import get_db

petugas_bp = Blueprint("petugas", __name__)


@petugas_bp.route("/petugas")
def petugas():
    role = session.get("role", "").lower()
    if role != "petugas":
        return redirect("/")

    db = get_db()

    try:

        checkin = db.table("transaksi").select("*").eq("status", "IN").execute().data
        checkout = db.table("transaksi").select("*").eq("status", "OUT").execute().data
        log = db.table("transaksi").select("*").eq("status", "DONE").execute().data

        print(f"DEBUG: Checkin count: {len(checkin)}")
        print(f"DEBUG: Data pertama checkin: {checkin[0] if checkin else 'Kosong'}")

        return render_template(
            "petugas_dashboard.html", checkin=checkin, checkout=checkout, log=log
        )

    except Exception as e:
        print(f"Error Database: {e}")
        return f"Terjadi kesalahan: {e}", 500
