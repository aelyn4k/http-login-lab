# HTTP Login Lab (Flask)

Aplikasi Flask sederhana untuk praktikum keamanan jaringan. Mahasiswa dapat mengamati alur login HTTP tanpa enkripsi, menyadap kredensial via Wireshark, dan menganalisis cookie sesi yang sengaja dibuat tidak aman. Proyek ini memakai MySQL sebagai sumber data pengguna (tabel `pengguna`).

## Persyaratan
- Python 3.10+
- MySQL Server (mis. XAMPP / MariaDB / MySQL Community)
- Pip packages: `flask`, `mysql-connector-python`

## Instalasi
1. **Clone & masuk ke folder proyek**
   ```bash
   git clone <repo-url>
   cd "Login Sederhana HTTP"
   ```
2. **(Opsional) Buat virtualenv**
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate  # PowerShell / CMD
   ```
3. **Install dependensi Python**
   ```bash
   pip install flask mysql-connector-python
   ```

## Menyiapkan Database
1. Jalankan MySQL Server.
2. Impor dump `weblogin_db.sql` untuk membuat database `weblogin_db` beserta tabel `pengguna` dan data contoh:
   ```bash
   mysql -u <user> -p < weblogin_db.sql
   ```
3. Pastikan tabel `pengguna` berisi minimal:

   | Username   | Password   |
   | ---------- | ---------- |
   | admin123   | admin12345 |
   | superadmin | admin12345 |
   | student    | wireshark  |

## Konfigurasi Lingkungan
Aplikasi membaca pengaturan koneksi dari environment variable berikut (nilai default di sisi kanan):
- `DB_HOST` (default `localhost`)
- `DB_PORT` (default `3306`)
- `DB_USER` (default `root`)
- `DB_PASSWORD` (default kosong)
- `DB_NAME` (default `weblogin_db`)
- `DB_TABLE` (default `pengguna`)
- `DB_USERNAME_FIELD` (default `username`)
- `DB_PASSWORD_FIELD` (default `password`)

Contoh set di PowerShell (hanya untuk sesi berjalan):
```powershell
$env:DB_HOST = "127.0.0.1"
$env:DB_USER = "root"
$env:DB_PASSWORD = "password_mysqlmu"
$env:DB_NAME = "weblogin_db"
$env:DB_TABLE = "pengguna"
$env:DB_USERNAME_FIELD = "username"
$env:DB_PASSWORD_FIELD = "password"
```

## Menjalankan Aplikasi
```bash
python app.py
```
Secara default server berjalan di `http://localhost:5051/`.

### Alur Demo
1. Buka `/login` dan masuk menggunakan salah satu kredensial pada tabel di atas.
2. Setelah sukses, Anda diarahkan ke dashboard dengan informasi modul praktikum dan cookie sesi.
3. Untuk keperluan lab, pantau trafik HTTP menggunakan Wireshark:
   - Gunakan filter `http.request || http.response`.
   - Temukan payload POST yang memuat username/password.
   - Observasi header `Set-Cookie` dan perhatikan atribut keamanannya.
4. Akses `http://localhost:5051/success` tanpa login akan men-redirect kembali ke halaman login.

## Catatan
- Session cookie (`session=user=...;insecure=true`) sengaja tidak diberi atribut `Secure`/`HttpOnly` untuk demonstrasi risiko.
- Proyek ini adalah materi latihan; jangan gunakan password nyata atau menjalankannya di lingkungan produksi.
- Untuk menambah akun baru, cukup sisipkan baris pada tabel `pengguna`.

## Lisensi
Gunakan bebas untuk kebutuhan edukasi; sesuaikan sesuai kebutuhan lab Anda.
