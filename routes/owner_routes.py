from flask import render_template, redirect, session, Blueprint
from config.db import get_db
from collections import Counter

owner_bp = Blueprint('owner', __name__)

@owner_bp.route('/owner')
def owner():
    if session.get('role')!="owner": return redirect('/')
    db = get_db()
    data = db.table("transaksi").select("*").order("id", desc=True).execute().data

    daily, status = [], []
    for t in data:
        if t.get('checkin_time'):
            daily.append(t['checkin_time'][:10])
        if t.get('status'):
            status.append(t['status'])

    return render_template(
        "owner_dashboard.html",
        data=data,
        daily_labels=list(Counter(daily).keys()),
        daily_count=list(Counter(daily).values()),
        status_labels=list(Counter(status).keys()),
        status_count=list(Counter(status).values())
    )