# 🚗 SmartParkingV3

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-IoT-purple?style=for-the-badge&logo=mqtt&logoColor=white)

**Sistem Manajemen Parkir Pintar** berbasis Python dengan arsitektur modular,
integrasi database real-time Supabase, dan komunikasi IoT via MQTT.

</div>

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Konfigurasi Environment](#-konfigurasi-environment-env)
- [Struktur Folder](#-struktur-folder)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Panduan Penggunaan Modul](#-panduan-penggunaan-modul)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)

---

## 🏢 Tentang Proyek

**SmartParkingV3** adalah aplikasi manajemen parkir berbasis web yang dirancang untuk mengelola data parkir secara **real-time**. Sistem ini dibangun menggunakan framework **Flask** dengan pola arsitektur **Blueprint** agar kode tetap terorganisir, modular, dan mudah dikembangkan.

Aplikasi ini mampu:

- Mengelola slot parkir secara dinamis
- Mencatat transaksi masuk/keluar kendaraan
- Mengintegrasikan sensor/perangkat IoT melalui protokol MQTT
- Menyajikan dashboard visual bagi Owner maupun Petugas Parkir

---

## ✨ Fitur Utama

| Modul               | Deskripsi                                                     |
| ------------------- | ------------------------------------------------------------- |
| 🔐 **Auth**         | Manajemen login, logout, dan sesi pengguna yang aman          |
| 📊 **Dashboard**    | Visualisasi data utama untuk Owner & Petugas secara real-time |
| 🅿️ **Parking**      | Pengelolaan slot parkir (tersedia, terisi, reserved)          |
| 💳 **Transaksi**    | Pencatatan dan kalkulasi biaya parkir otomatis                |
| 📡 **MQTT Handler** | Integrasi sensor/hardware ke sistem via protokol IoT          |

---

## 🛠️ Teknologi yang Digunakan

- **[Flask](https://flask.palletsprojects.com/)** — Web framework ringan berbasis Python
- **[Supabase](https://supabase.com/)** — Database PostgreSQL berbasis cloud dengan API real-time
- **[Paho-MQTT](https://pypi.org/project/paho-mqtt/)** — Library MQTT untuk komunikasi IoT
- **[Python Dotenv](https://pypi.org/project/python-dotenv/)** — Pengelolaan variabel environment
- **[Jinja2](https://jinja.palletsprojects.com/)** — Template engine HTML (bawaan Flask)

---

## ✅ Prasyarat

Sebelum memulai instalasi, pastikan sistem kamu sudah memiliki:

1. **Python 3.10 atau lebih baru**
   Cek versi Python yang terinstal:

    ```bash
    python --version
    ```

2. **PIP** (Python Package Installer)
   Biasanya sudah termasuk saat instalasi Python. Cek dengan:

    ```bash
    pip --version
    ```

3. **Akun Supabase**
   Daftar gratis di [supabase.com](https://supabase.com) dan buat project baru. Kamu akan memerlukan **URL** dan **API Key** dari project tersebut.

4. **Broker MQTT** _(opsional, diperlukan jika fitur IoT diaktifkan)_
   Bisa menggunakan broker lokal seperti [Mosquitto](https://mosquitto.org/) atau broker cloud seperti [HiveMQ](https://www.hivemq.com/).

> ⚠️ **Pengguna Windows:** Pastikan Python sudah ditambahkan ke **System PATH** agar perintah `python` dan `pip` bisa dijalankan dari mana saja di terminal.

---

## 🚀 Instalasi

Ikuti langkah-langkah berikut secara berurutan:

### Langkah 1 — Clone / Download Repositori

Clone repositori ini menggunakan Git:

```bash
git clone https://github.com/username/SmartparkingV3.git
```

Atau download sebagai file ZIP, lalu ekstrak. Kemudian masuk ke folder utama proyek:

```bash
cd SmartparkingV3
```

### Langkah 2 — (Opsional) Buat Virtual Environment

Sangat disarankan menggunakan virtual environment agar dependensi proyek tidak bercampur dengan paket Python sistem kamu:

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan — Windows
venv\Scripts\activate

# Aktifkan — macOS / Linux
source venv/bin/activate
```

Jika berhasil, nama environment `(venv)` akan muncul di awal baris terminal kamu.

### Langkah 3 — Instalasi Dependensi

Jalankan perintah berikut untuk menginstal semua library yang dibutuhkan:

```bash
pip install flask mysql-connector-python paho-mqtt supabase python-dotenv
```

Penjelasan masing-masing library:

| Library                  | Fungsi                                        |
| ------------------------ | --------------------------------------------- |
| `flask`                  | Web framework utama aplikasi                  |
| `mysql-connector-python` | Konektor MySQL (sebagai dependensi pendukung) |
| `paho-mqtt`              | Client MQTT untuk komunikasi IoT              |
| `supabase`               | SDK resmi untuk koneksi ke Supabase           |
| `python-dotenv`          | Membaca variabel dari file `.env`             |

> 📝 **Catatan:** `Blueprint` adalah fitur bawaan Flask dan **tidak perlu diinstal** secara terpisah.

---

## ⚙️ Konfigurasi Environment (`.env`)

File `.env` adalah tempat menyimpan **kredensial rahasia** aplikasi. File ini **tidak boleh** di-commit ke repositori publik (pastikan sudah ada di `.gitignore`).

### Cara Membuat File `.env`

Buat file baru bernama `.env` di **direktori utama** proyek (satu level dengan `app.py`):

```
SmartparkingV3/
├── app.py          ← app.py ada di sini
├── .env            ← buat file .env di sini
├── routes/
└── ...
```

### Isi File `.env`

Salin template berikut dan isi dengan data asli kamu:

```env
SUPABASE_URL=https://xyzabc.supabase.co   ← URL endpoint project Supabase kamu
SUPABASE_KEY=your_supabase_anon_key_here  ← API Key publik (anon key) dari Supabase untuk autentikasi
SECRET_KEY=supersecretkey                 ← Kunci rahasia Flask untuk enkripsi sesi pengguna
```

### Cara Mendapatkan Kredensial Supabase

1. Login ke [supabase.com](https://supabase.com) dan buka project kamu.
2. Klik menu **Project Settings** (ikon gear di sidebar kiri).
3. Pilih tab **API**.
4. Salin nilai **Project URL** → masukkan ke `SUPABASE_URL`.
5. Salin nilai **anon / public key** → masukkan ke `SUPABASE_KEY`.

> ⚠️ **Penting:** Pastikan `SUPABASE_URL` selalu diawali dengan `https://`. Tanpa protokol ini, koneksi ke database akan gagal.

### Penjelasan Variabel

| Variabel       | Deskripsi                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| `SUPABASE_URL` | URL endpoint project Supabase kamu (format: `https://xxx.supabase.co`)                               |
| `SUPABASE_KEY` | API Key publik (anon key) dari Supabase untuk autentikasi                                            |
| `SECRET_KEY`   | Kunci rahasia Flask untuk enkripsi sesi pengguna. Ganti dengan string acak yang kuat untuk produksi. |

---

## 📁 Struktur Folder

```
SmartparkingV3/
│
├── app.py                      # Entry point utama — mendaftarkan semua Blueprint & menjalankan server
├── mqtt_handler.py             # Logika komunikasi IoT via protokol MQTT
├── .env                        # Variabel environment rahasia (jangan di-commit!)
├── .gitignore                  # Daftar file yang diabaikan Git
├── requirements.txt            # (Opsional) Daftar dependensi proyek
│
├── routes/                     # Modul routing menggunakan Flask Blueprint
│   ├── __init__.py             # Inisialisasi package routes
│   ├── auth_router.py                 # Routing: Login, Logout, Manajemen Sesi
│   ├── dashboard_router.py            # Routing: Halaman utama Owner & Petugas
│   ├── parking_router.py              # Routing: Manajemen slot parkir
│   └── transaksi_router.py            # Routing: Pencatatan & kalkulasi biaya parkir
│
├── templates/                  # File HTML menggunakan template engine Jinja2
│   │── login.html              # Halaman login
│   ├── petugas_dashboard.html  # Halaman dashboard petugas
│   ├── owner_dashboard.html    # Halaman dashboard owner
│
└── static/                     # Aset statis
    ├── css/                    # File stylesheet (CSS)
    ├── js/                     # File JavaScript                 # Gambar dan ikon
```

### Penjelasan File & Folder Kunci

- **`app.py`**: Otak dari aplikasi. Di sinilah semua Blueprint dari folder `routes/` didaftarkan, konfigurasi Flask dimuat, dan server dijalankan.
- **`mqtt_handler.py`**: Mengelola koneksi ke broker MQTT, berlangganan (subscribe) ke topik tertentu, dan memproses pesan yang masuk dari sensor/perangkat keras.
- **`routes/`**: Setiap file di folder ini adalah sebuah **Blueprint** — unit routing yang mandiri dan terisolasi, memudahkan pengembangan fitur tanpa mengganggu bagian lain.
- **`templates/`**: Semua tampilan HTML dirender menggunakan Jinja2, yang memungkinkan penulisan logika dinamis langsung di dalam HTML.
- **`static/`**: Berisi semua file yang dikirim langsung ke browser tanpa pemrosesan server, seperti CSS, JavaScript, dan gambar.

---

## ▶️ Menjalankan Aplikasi

Setelah semua konfigurasi selesai, jalankan aplikasi dengan perintah:

```bash
python app.py
```

Jika berhasil, kamu akan melihat output seperti ini di terminal:

```
 * Running on http://127.0.0.1:8000
 * Debug mode: on
```

Buka browser dan akses:

```
http://127.0.0.1:8000
```

Aplikasi akan secara otomatis mengarahkan kamu ke **halaman login** (`auth.login`).

### Menghentikan Server

Tekan `Ctrl + C` di terminal untuk menghentikan server.

---

## 📖 Panduan Penggunaan Modul

### 🔐 Modul Auth (`routes/auth.py`)

Menangani semua proses autentikasi pengguna:

- **Login**: Verifikasi kredensial pengguna ke Supabase
- **Session Management**: Menyimpan informasi sesi pengguna secara aman menggunakan `SECRET_KEY`
- **Logout**: Menghapus sesi dan mengarahkan ke halaman login
- **Role-based Access**: Membedakan akses antara **Owner** dan **Petugas**

### 📊 Modul Dashboard (`routes/dashboard.py`)

Menyajikan tampilan utama setelah login:

- **Owner Dashboard**: Ringkasan statistik keseluruhan (total kendaraan, pendapatan, slot tersedia)
- **Petugas Dashboard**: Antarmuka operasional harian untuk mencatat kendaraan masuk/keluar

### 🅿️ Modul Parking (`routes/parking.py`)

Mengelola status slot parkir secara real-time:

- Menampilkan peta slot parkir (tersedia / terisi / reserved)
- Memperbarui status slot saat kendaraan masuk atau keluar
- Sinkronisasi data dengan Supabase secara langsung

### 💳 Modul Transaksi (`routes/transaksi.py`)

Mencatat setiap aktivitas parkir:

- Input data kendaraan (nomor plat, jenis kendaraan, waktu masuk)
- Kalkulasi biaya otomatis berdasarkan durasi parkir
- Riwayat transaksi yang dapat difilter dan diekspor

### 📡 MQTT Handler (`mqtt_handler.py`)

Jembatan antara perangkat keras dan sistem:

- Menerima sinyal dari sensor parkir (misal: sensor ultrasonik, RFID)
- Memproses data dan langsung memperbarui status slot di database
- Mendukung integrasi dengan berbagai platform IoT (ESP32, Arduino, Raspberry Pi)

---

## 🔧 Troubleshooting

### ❌ Error: Port 8000 Sudah Digunakan

Jika muncul pesan error `Address already in use`, berarti port 8000 sedang dipakai oleh proses lain.

**Solusi**: Ubah port di baris terakhir file `app.py`:

```python
# Ganti 8000 dengan port lain, misalnya 5000 atau 8080
app.run(debug=True, port=5000)
```

### ❌ Error: `ModuleNotFoundError`

Muncul ketika Python tidak bisa menemukan library yang dibutuhkan.

**Solusi**:

1. Pastikan semua library sudah terinstal tanpa error: `pip install flask mysql-connector-python paho-mqtt supabase python-dotenv`
2. Jika menggunakan virtual environment, pastikan sudah **diaktifkan** sebelum menjalankan `pip install` maupun `python app.py`.
3. **Windows:** Pastikan Python sudah ditambahkan ke System PATH saat proses instalasi.

### ❌ Error: Koneksi Database Gagal

Aplikasi tidak bisa terhubung ke Supabase.

**Solusi**:

1. Buka file `.env` dan pastikan `SUPABASE_URL` dimulai dengan `https://`.
2. Periksa kembali `SUPABASE_KEY` — pastikan tidak ada spasi atau karakter tersembunyi.
3. Coba akses URL Supabase kamu di browser untuk memastikan project aktif.
4. Periksa apakah IP kamu diblokir di pengaturan **Database > Connection Pooling** di Supabase.

### ❌ Error: MQTT Tidak Terhubung

**Solusi**:

1. Pastikan broker MQTT (misalnya Mosquitto) sudah berjalan di mesin yang sesuai.
2. Verifikasi host, port, dan kredensial broker di file konfigurasi MQTT.
3. Coba tes koneksi menggunakan tool MQTT Client seperti [MQTT Explorer](https://mqtt-explorer.com/).

---

## 🤝 Kontribusi

Kontribusi sangat terbuka! Jika ingin berkontribusi:

1. Fork repositori ini
2. Buat branch fitur baru: `git checkout -b fitur/nama-fitur`
3. Commit perubahan: `git commit -m 'Menambahkan fitur X'`
4. Push ke branch: `git push origin fitur/nama-fitur`
5. Buat Pull Request

---

<div align="center">

**Smart Parking System**

</div>
