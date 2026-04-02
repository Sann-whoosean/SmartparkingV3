from flask import Flask
from dotenv import load_dotenv
from config.db import get_db

load_dotenv()
from routes import register_blueprints
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "secret_dev")
SUPABASE_URL = os.environ.get("https://foxynxknymenhcaonxrl.supabase.co")
SUPABASE_KEY = os.environ.get("sb_publishable_0VDWVK7C-VSPHp9539BG5Q_YhYnyS0O")

register_blueprints(app)
print(f"DEBUG: URL={SUPABASE_URL}, KEY={SUPABASE_KEY}")
if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=False)  # Matikan reloader agar ringan
