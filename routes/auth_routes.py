from flask import request, render_template, redirect, session, Blueprint, jsonify
from config.db import get_db
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Gunakan form.get untuk data dari HTML
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            return render_template("login.html", msg="Isi semua field")

        db = get_db()
        try:
            res = db.table("users").select("*").eq("email", email).execute()
            user_data = res.data

            if user_data:
                user = user_data[0]

                if check_password_hash(user["password"], password):
                    session["role"] = user["role"].lower() if user.get("role") else ""
                    session["email"] = user["email"]
                    return redirect("/dashboard")

            return render_template("login.html", msg="Email / password salah")

        except Exception as e:
            return render_template("login.html", msg=f"Error: {str(e)}")

    # Method GET
    return render_template("login.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db()
    if not db:
        return jsonify({"error": "Koneksi database gagal"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"message": "Data tidak ditemukan"}), 400

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "petugas")

    if not email or not password:
        return jsonify({"message": "Email dan password wajib diisi"}), 400

    try:
        user_exists = db.table("users").select("email").eq("email", email).execute()
        if user_exists.data:
            return jsonify({"message": "Email sudah digunakan"}), 409

        hashed_password = generate_password_hash(password)

        new_user = {"email": email, "password": hashed_password, "role": role}

        result = db.table("users").insert(new_user).execute()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Akun berhasil dibuat!",
                    "user": result.data[0],
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
