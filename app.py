from flask import Flask, render_template, request, redirect, session, jsonify
from supabase import create_client
from datetime import datetime
from collections import Counter
from math import ceil
import hashlib, os
from dotenv import load_dotenv
from mqtt_handler import init_mqtt, mqtt_client

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secret_dev")

# ===== Supabase =====
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL atau SUPABASE_KEY belum di-set di .env")
else:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    try:
        # coba ambil data sederhana dari table users
        res = supabase.table("users").select("*").limit(2).execute()
        if res.data is not None:
            print("✅ Koneksi ke Supabase berhasil!")
            print("Contoh data:", res.data)
        else:
            print("⚠️ Koneksi oke, tapi table 'users' kosong atau query gagal")
    except Exception as e:
        print("❌ Gagal koneksi:", e)

def get_db():
    return supabase

# ===== MQTT =====
import paho.mqtt.client as mqtt
from mqtt_handler import init_mqtt

mqtt_client = mqtt.Client(client_id="")
init_mqtt(mqtt_client)

mqtt_client.connect("broker.hivemq.com", 1883)
mqtt_client.loop_start()
# ===== LOGIN =====
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','').strip()
        if not email or not password:
            return render_template("login.html", msg="Isi semua field")

        db = get_db()
        res = db.table("users").select("*").eq("email", email).execute()
        users = res.data  # <- harus ambil dari res.data

        if users:
            user = users[0]
            hashed_input = hashlib.md5(password.encode()).hexdigest()
            print("DB password:", user['password'], "Input hash:", hashed_input)
            print("Role:", user['role'])
            if hashed_input == user['password']:
                session['role'] = user['role'].lower() if user['role'] else ''
                session['email'] = user['email']
                return redirect('/dashboard')
            else:
                print("Password tidak cocok")
        else:
            print("Email tidak ditemukan")

        return render_template("login.html", msg="Email / password salah")

    return render_template("login.html")

# ===== LOGOUT =====
@app.route('/logout')
def logout():
    session.clear()   # hapus semua session
    return redirect('/')
    
# ===== DASHBOARD =====
@app.route('/dashboard')
def dashboard():
    role = session.get('role','')
    if role=="owner": return redirect('/owner')
    if role=="petugas": return redirect('/petugas')
    return redirect('/')

@app.route('/owner')
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

@app.route('/petugas')
def petugas():
    if session.get('role')!="petugas": return redirect('/')
    db = get_db()
    checkin = db.table("transaksi").select("*").eq("status","IN").execute().data
    checkout = db.table("transaksi").select("*").eq("status","OUT").execute().data
    log = db.table("transaksi").select("*").eq("status","DONE").execute().data
    return render_template("petugas_dashboard.html", checkin=checkin, checkout=checkout, log=log)

# ===== CHECKIN =====
@app.route('/checkin/<rfid>')
def checkin(rfid):
    if len(rfid)<5: return "RFID tidak valid"
    now = datetime.now().isoformat()
    db = get_db()
    db.table("transaksi").insert({"card_id":rfid, "checkin_time":now, "status":"IN"}).execute()
    try:
        if mqtt_client.is_connected():
            mqtt_client.publish("parking/sandy/entry/servo","OPEN")
            mqtt_client.publish("parking/sandy/lcd","Selamat Datang")
    except: pass
    return f"Checkin berhasil {rfid}"

# ===== CHECKOUT =====
@app.route('/checkout/<rfid>')
def checkout(rfid):
    db = get_db()
    res = db.table("transaksi").select("*").eq("card_id",rfid).eq("status","IN").order("checkin_time",desc=True).limit(1).execute()
    data_list = res.data
    if not data_list: return "Kendaraan tidak ditemukan"

    data = data_list[0]
    checkin_time = datetime.fromisoformat(data['checkin_time'])
    now = datetime.now()
    durasi_jam = ceil((now-checkin_time).total_seconds()/3600)
    if durasi_jam<1: durasi_jam=1
    fee = durasi_jam*2000
    durasi_menit = ceil((now-checkin_time).total_seconds()/60)

    db.table("transaksi").update({
        "checkout_time": now.isoformat(),
        "duration": durasi_menit,
        "fee": fee,
        "status":"OUT"
    }).eq("id", data['id']).execute()

    try:
        if mqtt_client.is_connected():
            mqtt_client.publish("parking/sandy/lcd", f"Biaya Rp{fee}")
    except: pass

    return f"<script>alert('Checkout berhasil. Biaya Rp{fee}');window.location='/petugas';</script>"

# ===== BUKA EXIT =====
@app.route('/buka-exit/<rfid>')
def buka_exit(rfid):
    db = get_db()
    res = db.table("transaksi").select("*").eq("card_id",rfid).eq("status","OUT").order("checkout_time",desc=True).limit(1).execute()
    if not res.data:
        return "<script>alert('Transaksi tidak ditemukan');window.location='/petugas';</script>"
    t = res.data[0]
    fee = t.get('fee',0)
    db.table("transaksi").update({"status":"DONE"}).eq("id", t['id']).execute()
    try:
        if mqtt_client.is_connected():
            mqtt_client.publish("parking/sandy/exit/servo","OPEN")
            mqtt_client.publish("parking/sandy/lcd", f"Terima Kasih. Rp{fee}")
    except: pass
    return f"<script>alert('Gerbang exit dibuka. Biaya Rp{fee}');window.location='/petugas';</script>"

# ===== API =====
@app.route('/api/transaksi')
def api():
    db = get_db()
    checkin = db.table("transaksi").select("*").eq("status","IN").execute().data
    checkout = db.table("transaksi").select("*").eq("status","OUT").execute().data
    log = db.table("transaksi").select("*").eq("status","DONE").execute().data
    return jsonify({"checkin":checkin,"checkout":checkout,"log":log})

# ===== TEST MQTT =====
@app.route('/test-mqtt')
def test():
    try:
        mqtt_client.publish("smartparking/test","HELLO")
        return "MQTT OK"
    except Exception as e:
        return str(e)

if __name__=="__main__":
    app.run(debug=True)