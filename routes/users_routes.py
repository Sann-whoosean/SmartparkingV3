from flask import Blueprint, request, jsonify
from config.db import get_db

users_bp = Blueprint("users", __name__)


class Users:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.table("users").select("*").execute().data

    def get_by_id(self, user_id):
        result = self.db.table("users").select("*").eq("id", user_id).execute()
        return result.data[0] if result.data else None


@users_bp.route("/users", methods=["GET"])
def get_users():
    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    user_service = Users(db)
    try:
        data = user_service.get_all()
        return jsonify({"status": "success", "count": len(data), "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_detail(user_id):
    db = get_db()
    user_service = Users(db)

    try:
        user = user_service.get_by_id(user_id)
        if not user:
            return jsonify({"message": "User tidak ditemukan"}), 404

        return jsonify({"status": "success", "data": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
