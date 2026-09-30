"""Modul backend autentikasi Flask dengan antarmuka web interaktif."""

import sqlite3
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def init_db():
    """Inisialisasi basis data dan membuat data pengguna awal."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES ('admin', 'supersecret')"
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    """Menampilkan formulir login dan memproses autentikasi."""
    message = None
    status_class = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        # Parameterized query untuk mencegah SQL Injection
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            message = "Login Berhasil! Selamat datang."
            status_class = "success"
        else:
            message = "Login Gagal! Kredensial tidak valid."
            status_class = "danger"

    return render_template(
        "index.html", message=message, status_class=status_class
    )


@app.route("/health", methods=["GET"])
def health():
    """Endpoint pengecekan status aplikasi (health check)."""
    return jsonify(
        status="ok",
        service="secure-flask-app",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.route("/about", methods=["GET"])
def about():
    """Menampilkan informasi singkat tentang aplikasi."""
    return jsonify(
        name="Secure Flask App",
        description="Demo pipeline DevSecOps dengan GitHub Actions",
        pipeline=["Semgrep SAST", "Pylint", "Docker", "Auto Deploy"],
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)  # nosemgrep