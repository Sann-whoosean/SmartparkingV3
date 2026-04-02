import json
import time
from datetime import datetime

mqtt_client = None

# anti spam RFID
last_data = {}
last_time = {}
COOLDOWN = 3  # detik


def init_mqtt(client):
    global mqtt_client
    mqtt_client = client
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message


def on_connect(client, userdata, flags, reasonCode, properties=None):
    print(f"[MQTT] CONNECTED WITH CODE: {reasonCode}")
    # Subscribe ke semua topik yang diperlukan
    client.subscribe("parking/sandy/entry/rfid")
    client.subscribe("parking/sandy/exit/rfid")
    client.subscribe("parking/sandy/entry/servo")
    client.subscribe("parking/sandy/exit/servo")
    client.subscribe("parking/sandy/lcd")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode().strip()
    now = time.time()

    # ================= RFID LOGIC =================
    if "rfid" in topic:
        try:
            data = json.loads(payload)
            rfid = data.get("rfid")
            if not rfid:
                return

            key = topic
            # Anti-spam logic
            if key in last_data:
                if last_data[key] == rfid and (now - last_time[key]) < COOLDOWN:
                    return

            last_data[key] = rfid
            last_time[key] = now

            handle_rfid(topic, rfid)

        except Exception as e:
            print(f"[MQTT ERROR] RFID Payload semi-invalid: {e}")

    elif "servo" in topic:
        if payload == "OPEN":
            handle_servo(topic)

    elif "lcd" in topic:
        handle_lcd(payload)


# ================= CORE LOGIC =================


def handle_rfid(topic, rfid):
    global mqtt_client
    if not mqtt_client:
        return

    try:
        # Perbaikan Import: Ambil langsung dari config, bukan dari app
        from config.db import get_db
        from datetime import datetime
        from math import ceil

        db = get_db()

        # ================= ENTRY =================
        if "entry" in topic:
            print(f"[LOG] Mencoba Check-in RFID: {rfid}")

            # Cek apakah sudah ada di dalam
            exist = (
                db.table("transaksi")
                .select("*")
                .eq("card_id", rfid)
                .eq("status", "IN")
                .execute()
                .data
            )

            if exist:
                print(f"[LOG] RFID {rfid} ditolak: Masih berstatus IN.")
                mqtt_client.publish("parking/sandy/lcd", "Sudah Check-in|Gagal Masuk")
                return

            # Insert Data Baru
            db.table("transaksi").insert(
                {
                    "card_id": rfid,
                    "status": "IN",
                    "checkin_time": datetime.now().isoformat(),
                }
            ).execute()

            print(f"[LOG] RFID {rfid} Berhasil Check-in.")
            mqtt_client.publish("parking/sandy/entry/servo", "OPEN")
            mqtt_client.publish("parking/sandy/lcd", "Selamat Datang|Silakan Masuk")

        # ================= EXIT =================
        elif "exit" in topic:
            print(f"[LOG] Mencoba Check-out RFID: {rfid}")
            rfid_clean = rfid.strip()

            # 1. Cari data IN
            res = (
                db.table("transaksi")
                .select("*")
                .eq("card_id", rfid_clean)
                .eq("status", "IN")
                .order("checkin_time", desc=True)
                .limit(1)
                .execute()
            )

            if not res.data:
                print(
                    f"[LOG] RFID {rfid_clean} tidak ditemukan (Mungkin sudah OUT/DONE)"
                )
                mqtt_client.publish("parking/sandy/lcd", "Kartu Tidak|Terdaftar")
                return

            data = res.data[0]
            checkin_time = datetime.fromisoformat(data["checkin_time"])
            now = datetime.now()

            # 2. Hitung Biaya & Durasi
            from math import ceil  # Pastikan ini ada

            selisih_detik = (now - checkin_time).total_seconds()
            durasi_menit = ceil(selisih_detik / 60)
            durasi_jam = ceil(selisih_detik / 3600)

            if durasi_jam < 1:
                durasi_jam = 1

            fee = durasi_jam * 2000

            # 3. SATU KALI UPDATE SAJA (Lebih Aman & Pasti Berubah)
            try:
                update_req = (
                    db.table("transaksi")
                    .update(
                        {
                            "checkout_time": now.isoformat(),
                            "duration": durasi_menit,
                            "fee": fee,
                            "status": "OUT",
                        }
                    )
                    .eq("id", data["id"])
                    .execute()
                )
                if len(update_req.data) > 0:
                    print(
                        f"[LOG] DATABASE UPDATED: {update_req.data[0]['status']} for ID {data['id']}"
                    )
                    mqtt_client.publish("parking/sandy/lcd", f"Lunas|Rp {fee}")
                else:
                    print(
                        f"[ERROR] Update gagal! Data tidak ditemukan atau RLS menghalangi ID: {data['id']}"
                    )
            except Exception as e:
                (f"[SYSTEM ERROR] Gagal eksekusi update: {e}")
    except Exception as e:
        print(f"[SYSTEM ERROR] Gagal eksekusi update: {e}")


def handle_servo(topic):
    print(f"[LOG] Servo Command: {topic} is OPENING")


def handle_lcd(payload):
    # Log untuk memantau apa yang tampil di layar alat
    print(f"[LOG] LCD Display: {payload}")
