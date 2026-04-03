from flask import Flask, redirect, url_for
from dotenv import load_dotenv


load_dotenv()
from routes import register_blueprints
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret_dev")


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)
