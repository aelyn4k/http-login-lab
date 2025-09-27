import os
import string

from flask import Flask, request, render_template, redirect, url_for, make_response
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "weblogin_db"),
    "port": int(os.getenv("DB_PORT", 3306)),
}


def _safe_identifier(candidate: str, fallback: str) -> str:
    allowed = string.ascii_letters + string.digits + "_"
    value = candidate or fallback
    if not value:
        return fallback
    if value[0].isdigit():
        return fallback
    if any(ch not in allowed for ch in value):
        return fallback
    return value


TABLE_NAME = _safe_identifier(os.getenv("DB_TABLE"), "pengguna")
USER_COLUMN = _safe_identifier(os.getenv("DB_USERNAME_FIELD"), "username")
PASSWORD_COLUMN = _safe_identifier(os.getenv("DB_PASSWORD_FIELD"), "password")


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_user(username):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = (
            f"SELECT {USER_COLUMN} AS username, {PASSWORD_COLUMN} AS password "
            f"FROM {TABLE_NAME} WHERE {USER_COLUMN} = %s LIMIT 1"
        )
        cursor.execute(query, (username,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET"])
def login():
    # tampilkan error inline jika ada ?err=
    err = request.args.get("err")
    return render_template("login.html", err=err)

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    username = username.strip()

    try:
        record = fetch_user(username)
    except Error:
        return redirect(url_for("failed", err="Gagal terhubung ke database."))

    if record and record.get("password") == password:
        resp = make_response(redirect(url_for("success")))
        # Cookie sengaja tidak aman (tanpa Secure/HttpOnly) untuk demo
        resp.set_cookie("session", f"user={username};insecure=true")
        return resp

    return redirect(url_for("failed", err="Username/Password salah"))

@app.route("/success", methods=["GET"])
def success():
    raw_cookie = request.cookies.get("session", "")
    if not raw_cookie:
        return redirect(url_for("login", err="Silakan login terlebih dahulu."))

    parts = {}
    for fragment in raw_cookie.split(";"):
        fragment = fragment.strip()
        if "=" in fragment:
            key, value = fragment.split("=", 1)
            parts[key] = value

    username = parts.get("user")
    if not username:
        return redirect(url_for("login", err="Sesi tidak valid, silakan login ulang."))

    lab_modules = [
        {
            "icon": "🌐",
            "title": "HTTP Basic Flow",
            "desc": "Analisis request/response login sederhana dan kenali kredensial yang terkirim."
        },
        {
            "icon": "📡",
            "title": "Packet Capture",
            "desc": "Tangkap paket dengan Wireshark dan tandai paket POST serta cookie balasannya."
        },
        {
            "icon": "🛡",
            "title": "Mitigasi",
            "desc": "Diskusikan bagaimana HTTPS dan cookie aman mencegah kebocoran kredensial."
        }
    ]

    capture_steps = [
        "Buka Wireshark lalu pilih interface jaringan lab kamu.",
        "Gunakan filter display `http.request || http.response` untuk fokus pada traffic inti.",
        "Login menggunakan kredensial demo dan perhatikan payload POST.",
        "Cari Set-Cookie pada response dan catat atribut keamanannya."
    ]

    resources = [
        {
            "label": "Cheat sheet filter Wireshark",
            "href": "https://wiki.wireshark.org/DisplayFilters",
            "type": "Artikel"
        },
        {
            "label": "RFC 6265 - HTTP State Management",
            "href": "https://www.rfc-editor.org/rfc/rfc6265",
            "type": "Standar"
        },
        {
            "label": "OWASP Transport Layer Protection Cheat Sheet",
            "href": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html",
            "type": "OWASP"
        }
    ]

    return render_template(
        "dashboard.html",
        username=username,
        cookie=raw_cookie or "(tidak ada cookie)",
        modules=lab_modules,
        steps=capture_steps,
        resources=resources,
    )

@app.route("/failed", methods=["GET"])
def failed():
    err = request.args.get("err", "Login gagal.")
    return render_template("failed.html", err=err)

if __name__ == "__main__":
    # Jalankan HTTP polos (tanpa HTTPS). Port 5051 supaya tidak tabrakan dengan server lama.
    app.run(host="0.0.0.0", port=5051, debug=False)
