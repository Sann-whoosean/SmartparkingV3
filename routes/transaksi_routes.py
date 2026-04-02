from flask import Blueprint, jsonify
from config.db import get_db

transaksi_bp = Blueprint("transaksi", __name__)


@transaksi_bp.route("/transaksi")
def transaksi():
    db = get_db()
    checkin = db.table("transaksi").select("*").eq("status", "IN").execute().data
    checkout = db.table("transaksi").select("*").eq("status", "OUT").execute().data
    log = db.table("transaksi").select("*").eq("status", "DONE").execute().data
    return jsonify({"checkin": checkin, "checkout": checkout, "log": log})
