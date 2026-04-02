from flask import Blueprint, render_template, redirect, session, jsonify
from config.db import get_db

petugas_bp = Blueprint('petugas', __name__)
@petugas_bp.route('/petugas')
def petugas():
    if session.get('role')!="petugas": return redirect('/')
    db = get_db()
    checkin = db.table("transaksi").select("*").eq("status","IN").execute().data
    checkout = db.table("transaksi").select("*").eq("status","OUT").execute().data
    log = db.table("transaksi").select("*").eq("status","DONE").execute().data
    return render_template("petugas_dashboard.html", checkin=checkin, checkout=checkout, log=log)
