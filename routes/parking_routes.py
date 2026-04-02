from flask import Blueprint, jsonify
from config.db import get_db

parking_bp = Blueprint("parking", __name__)


class ParkingRoutes:
    def __init__(self, db):
        self.db = db

    def getParking(self):
        res = self.db.table("transaksi").select("*").execute()
        return res.data


@parking_bp.route("/get_parking")
def getParking():
    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    parking_routes = ParkingRoutes(db)
    
    try:
        data = parking_routes.getParking()
        
        if data is None:
            data = []

        return jsonify({
            "status": "success", 
            "count": len(data), 
            "data": data
        }), 200
    except Exception as e:
        print(f"[ERROR] get_parking: {e}") # Log ke terminal untuk debug
        return jsonify({"error": str(e)}), 500