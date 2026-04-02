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
    print("MQTT CONNECTED:", reasonCode)

    client.subscribe("parking/sandy/entry/rfid")
    client.subscribe("parking/sandy/exit/rfid")
    client.subscribe("parking/sandy/entry/servo")
    client.subscribe("parking/sandy/exit/servo")
    client.subscribe("parking/sandy/lcd")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode().strip()

    print(f"[MQTT] {topic} -> {payload}")

    now = time.time()

    # ================= RFID =================
    if "rfid" in topic:
        try:
            data = json.loads(payload)
            rfid = data.get("rfid")

            if not rfid:
                return

            key = topic

            # anti spam
            if key in last_data:
                if last_data[key] == rfid and (now - last_time[key]) < COOLDOWN:
                    return

            last_data[key] = rfid
            last_time[key] = now

            handle_rfid(topic, rfid)

        except Exception as e:
            print("RFID ERROR:", e)

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
        from app import get_db
        db = get_db()

        # ================= ENTRY =================
        if "entry" in topic:
            print("[ENTRY RFID]", rfid)

            exist = db.table("transaksi") \
                .select("*") \
                .eq("card_id", rfid) \
                .eq("status", "IN") \
                .execute().data

            if exist:
                print("Sudah checkin, skip")
                return

            db.table("transaksi").insert({
                "card_id": rfid,
                "status": "IN",
                "checkin_time": datetime.now().isoformat()
            }).execute()

            mqtt_client.publish("parking/sandy/entry/servo", "OPEN")
            mqtt_client.publish("parking/sandy/lcd", "Selamat Datang")

        # ================= EXIT =================
        elif "exit" in topic:
            print("[EXIT RFID]", rfid)

            res = db.table("transaksi") \
                .select("*") \
                .eq("card_id", rfid) \
                .eq("status", "IN") \
                .order("checkin_time", desc=True) \
                .limit(1) \
                .execute()

            data = res.data

            if not data:
                print("Tidak ada data IN untuk RFID ini")
                return

            record = data[0]
            print("EXIT RECORD:", record)

            update = db.table("transaksi") \
                .update({
                    "status": "OUT",
                    "checkout_time": datetime.now().isoformat()
                }) \
                .eq("id", record["id"]) \
                .execute()

            print("UPDATE RESULT:", update)

            mqtt_client.publish("parking/sandy/exit/servo", "OPEN")
            mqtt_client.publish("parking/sandy/lcd", "Terima Kasih")

    except Exception as e:
        print("HANDLE RFID ERROR:", e)


def handle_servo(topic):
    print("[SERVO]", topic)


def handle_lcd(payload):
    try:
        if "|" in payload:
            line1, line2 = payload.split("|", 1)
            print("[LCD]", line1, "|", line2)
        else:
            print("[LCD]", payload)
    except:
        print("LCD ERROR")