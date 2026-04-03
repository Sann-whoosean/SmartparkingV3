# from flask import Blueprint
# from config.db import get_db
# from datetime import datetime
# from math import ceil
# from config.mqtt import mqtt_client
# from flask import Blueprint

# handler_bp = Blueprint("handler", __name__)


# # ===== CHECKIN =====
# @handler_bp.route("/checkin/<rfid>")
# def checkin(rfid):
#     rfid_clean = rfid.upper().strip()
#     print(rfid_clean)
#     if len(rfid_clean) < 5:
#         return "RFID tidak valid"

#     db = get_db()

#     try:
#         existing_user = (
#             db.table("transaksi")
#             .select("id")
#             .eq("card_id", rfid_clean)
#             .eq("status", "IN")
#             .execute()
#         )

#         if existing_user.data:
#             # Jika data ditemukan, berarti mobilnya masih di dalam
#             print(f"[LOG] RFID {rfid_clean} mencoba masuk, tapi status masih IN.")
#             return f"Kartu {rfid_clean} sudah berada di dalam area parkir!"

#         # 2. Jika tidak ada (data kosong), silakan Check-in
#         now = datetime.now().isoformat()
#         db.table("transaksi").insert(
#             {"card_id": rfid_clean, "checkin_time": now, "status": "IN"}
#         ).execute()

#         print(f"[LOG] RFID {rfid_clean} BERHASIL Check-in.")

#         # 3. Trigger Hardware
#         if mqtt_client.is_connected():
#             mqtt_client.publish("parking/sandy/entry/servo", "OPEN")
#             mqtt_client.publish("parking/sandy/lcd", "Selamat Datang")

#         return f"Checkin berhasil {rfid_clean}"

#     except Exception as e:
#         print(f"[ERROR] Gagal proses check-in: {e}")
#         return f"Terjadi kesalahan sistem: {str(e)}"


# # ===== CHECKOUT =====
# @handler_bp.route("/checkout/<rfid>")
# def checkout(rfid):
#     rfid_clean = rfid.upper().strip()
#     db = get_db()
#     print(rfid_clean)
#     res = (
#         db.table("transaksi")
#         .select("*")
#         .eq("card_id", rfid_clean)
#         .eq("status", "IN")
#         .order("checkin_time", desc=True)
#         .limit(1)
#         .execute()
#     )

#     if not res.data:
#         return "Kendaraan tidak ditemukan atau sudah checkout"

#     data = res.data[0]
#     checkin_time = datetime.fromisoformat(data["checkin_time"])
#     now = datetime.now()

#     selisih_detik = (now - checkin_time).total_seconds()
#     durasi_menit = ceil(selisih_detik / 60)
#     durasi_jam = ceil(selisih_detik / 3600)

#     if durasi_jam < 1:
#         durasi_jam = 1

#     fee = durasi_jam * 2000

#     err = (
#         db.table("transaksi")
#         .update(
#             {
#                 "checkout_time": now.isoformat(),
#                 "duration": durasi_menit,
#                 "fee": fee,
#                 "status": "OUT",
#             }
#         )
#         .eq("id", data["id"])
#         .execute()
#     )
#     print(f"[LOG] Checkout {rfid_clean} {err.data}")

#     if not err.data:
#         return "Gagal update data checkout"
#     try:
#         if mqtt_client.is_connected():
#             mqtt_client.publish("parking/sandy/lcd", f"Biaya Rp{fee}")
#     except:
#         pass

#     return f"<script>alert('Checkout berhasil. Biaya Rp{fee}');window.location='/petugas';</script>"


# # ===== BUKA EXIT =====
# @handler_bp.route("/buka-exit/<rfid>")
# def buka_exit(rfid):
#     db = get_db()
#     rfid_clean = rfid.upper().strip()

#     res = (
#         db.table("transaksi")
#         .select("*")
#         .eq("card_id", rfid_clean)
#         .eq("status", "OUT")
#         .order("id", desc=True)
#         .limit(1)
#         .execute()
#     )

#     if not res.data:
#         return "<script>alert('Data OUT tidak ditemukan. Silakan check-out dulu!');window.location='/petugas';</script>"

#     t = res.data[0]
#     fee = t.get("fee", 0)

#     try:
#         # Update jadi DONE agar tidak bisa disalahgunakan
#         db.table("transaksi").update({"status": "DONE"}).eq("id", t["id"]).execute()

#         if mqtt_client.is_connected():
#             mqtt_client.publish("parking/sandy/exit/servo", "OPEN")
#             mqtt_client.publish("parking/sandy/lcd", f"Lunas. Rp{fee}")

#         return f"<script>alert('Gerbang dibuka. Status DONE. Biaya Rp{fee}');window.location='/petugas';</script>"

#     except Exception as e:
#         return f"<script>alert('Gagal update status: {str(e)}');window.location='/petugas';</script>"
