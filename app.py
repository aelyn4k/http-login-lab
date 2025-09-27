from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

# Kredensial demo (plaintext untuk edukasi)
VALID_USER = {"username": "student", "password": "wireshark"}


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

    # Akan terlihat jelas di payload HTTP (untuk Wireshark)
    if username == VALID_USER["username"] and password == VALID_USER["password"]:
        resp = make_response(redirect(url_for("success")))
        # Cookie sengaja tidak aman (tanpa Secure/HttpOnly) untuk demo
        resp.set_cookie("session", f"user={username};insecure=true")
        return resp
    else:
        # Pilihan 1 (inline message): return redirect(url_for("login", err="Username/Password salah"))
        # Pilihan 2 (halaman gagal):
        return redirect(url_for("failed", err="Username/Password salah"))

@app.route("/success", methods=["GET"])
def success():
    user_cookie = request.cookies.get("session", "(tidak ada cookie)")
    return render_template("success.html", cookie=user_cookie)

@app.route("/failed", methods=["GET"])
def failed():
    err = request.args.get("err", "Login gagal.")
    return render_template("failed.html", err=err)

if __name__ == "__main__":
    # Jalankan HTTP polos (tanpa HTTPS). Port 5051 supaya tidak tabrakan dengan server lama.
    app.run(host="0.0.0.0", port=5051, debug=False)
