from flask import Blueprint, jsonify, request
from config.db import get_db

parking_bp = Blueprint("parking", __name__)


class ParkingRoutes:
    def __init__(self, db):
        self.db = db

    def get_all_parking(self):
        res = self.db.table("transaksi").select("*").execute()
        return res.data

    def get_parking_by_id(self, id):
        res = self.db.table("transaksi").select("*").eq("id", id).execute()
        return res.data[0] if res.data else None


# --- Routes ---


@parking_bp.route("/parking", methods=["GET"])
def get_all_parking_route():
    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    handler = ParkingRoutes(db)
    try:
        data = handler.get_all_parking()
        return (
            jsonify(
                {
                    "status": "success",
                    "count": len(data) if data else 0,
                    "data": data or [],
                }
            ),
            200,
        )
    except Exception as e:
        print(f"[ERROR] get_all_parking: {e}")
        return jsonify({"error": str(e)}), 500


@parking_bp.route("/parking/<int:id>", methods=["GET"])
def get_parking_by_id_route(id):
    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    handler = ParkingRoutes(db)
    try:
        data = handler.get_parking_by_id(id)

        if data is None:
            return jsonify({"status": "error", "message": "Data not found"}), 404

        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        print(f"[ERROR] get_parking_by_id: {e}")
        return jsonify({"error": str(e)}), 500


@parking_bp.route("/parking/<int:id>", methods=["PUT"])
def update_parking_route(id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        response = db.table("transaksi").update(data).eq("id", int(id)).execute()

        if not response.data:
            return (
                jsonify(
                    {
                        "error": f"Data dengan ID {id} tidak ditemukan",
                        "details": str(response),
                        "debug_info": "Check if ID exists in table 'transaksi'",
                    }
                ),
                404,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "count": len(response.data),
                    "data": response.data,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"[ERROR] update_parking: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
