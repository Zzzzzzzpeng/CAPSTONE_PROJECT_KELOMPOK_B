# 🐟 Sumber Aquarium PGK

### Sistem Informasi Pengelolaan Toko Ikan Hias

**Capstone Project — Program Studi S1 Sistem Informasi, Universitas Terbuka**

> **Satu sistem. Satu alur data. Satu pusat informasi operasional.**

Sumber Aquarium PGK adalah aplikasi web yang dikembangkan oleh **Kelompok B** sebagai proyek akademik pada bidang Sistem Informasi. Sistem ini dirancang untuk membantu pengelolaan operasional toko ikan hias melalui integrasi **data persediaan ikan, transaksi penjualan, pencatatan kematian ikan, riwayat operasional, dashboard, dan autentikasi pengguna** dalam satu aplikasi.

Project ini menghubungkan antarmuka web dengan backend Flask dan database PostgreSQL menggunakan pendekatan client-server sederhana yang berfokus pada integrasi data dan proses bisnis.

---

## 🎓 Tentang Project

Universitas Terbuka menjelaskan Capstone Project sebagai tahap akhir pembelajaran yang memberi kesempatan kepada mahasiswa untuk menerapkan pengetahuan dan keterampilan akademik dalam penyelesaian permasalahan nyata melalui perancangan, implementasi, dan evaluasi sistem informasi. Pendekatan tersebut menjadi dasar akademik bagi pengembangan Sumber Aquarium PGK sebagai proyek kelompok pada Program Studi S1 Sistem Informasi.

Project ini tidak hanya berfokus pada tampilan antarmuka, tetapi juga mencakup:

* perancangan struktur database;
* implementasi backend dan API;
* autentikasi berbasis session;
* validasi data;
* pengelolaan stok;
* transaksi penjualan;
* pencatatan mortalitas ikan;
* histori operasional;
* integrasi frontend dan backend;
* dokumentasi proyek.

---

## 👥 Kelompok B

### Universitas Terbuka — S1 Sistem Informasi

| Anggota                  | NIM         | Peran dalam Project                                                                                            |
| ------------------------ | ----------- | -------------------------------------------------------------------------------------------------------------- |
| **DIMAS**                | `050039851` | **Fondasi Sistem & Data** — kontribusi pada fondasi awal HTML, CSS, JavaScript, serta data pendukung proyek    |
| **DHEA HANDANUR AINI**   | `050417407` | **Dokumentasi & Proposal** — penyusunan proposal dan dokumentasi proyek untuk kebutuhan akademik               |
| **KAMALUDIN**            | `050595262` | **Komunikasi Visual & Presentasi** — materi presentasi, poster, dan penyampaian visual proyek                  |
| **MUHAMAD ARPAN KURNIA** | `051102736` | **Full-Stack & System Integration** — integrasi frontend, API, database, autentikasi, security, dan deployment |



---

## 🎯 Tujuan Sistem

Sumber Aquarium PGK dikembangkan untuk menyediakan satu alur informasi operasional yang lebih terstruktur.

Fokus utama sistem:

* 🐟 mengelola data dan jumlah stok ikan;
* 🛒 mencatat transaksi penjualan;
* ⚠️ mencatat kejadian kematian ikan;
* 📋 menyediakan histori penjualan dan kematian;
* 📊 menampilkan ringkasan operasional melalui dashboard;
* 🔐 membatasi akses sistem melalui autentikasi pengguna;
* 🗄️ menyimpan data terpusat pada PostgreSQL.

---

## 🧩 Fitur Sistem

### 📊 Dashboard

Dashboard menyajikan ringkasan:

* total persediaan ikan;
* jumlah jenis ikan;
* jumlah transaksi;
* jumlah kejadian kematian;
* jumlah stok dengan batas perhatian;
* nilai akumulasi penjualan;
* lima transaksi penjualan terakhir;
* lima kejadian kematian terakhir;
* status sesi pengguna;
* waktu sinkronisasi sesi.

Data dashboard diperoleh melalui API server dan dihitung di sisi frontend.

---

### 🐟 Manajemen Stok Ikan

Modul stok menyediakan:

* daftar seluruh ikan;
* ID ikan;
* nama ikan;
* kategori;
* jumlah stok;
* harga satuan;
* pencarian berdasarkan nama atau kategori;
* penghapusan data ikan.

Data stok berasal dari tabel `ikan` pada PostgreSQL.

---

### ➕ Tambah Ikan

Modul tambah ikan menerima:

* nama ikan;
* kategori;
* stok awal;
* harga satuan.

Foto default sistem menggunakan:

```text
/assets/images/logo.png
```

Data dikirim ke backend melalui `POST /api/ikan`.

---

### 🛒 Pencatatan Penjualan

Transaksi penjualan menerima:

* ikan yang dipilih;
* jumlah ikan terjual.

Backend kemudian:

1. memeriksa keberadaan ikan;
2. mengunci row ikan;
3. memeriksa kecukupan stok;
4. menghitung total harga;
5. mengurangi stok;
6. menyimpan histori transaksi.

Proses tersebut dilakukan di dalam transaksi database.

---

### ⚠️ Pencatatan Kematian

Modul mortalitas menerima:

* ikan;
* jumlah ikan mati;
* keterangan penyebab atau kondisi.

Backend kemudian:

1. memeriksa ikan;
2. mengunci row ikan;
3. memeriksa stok;
4. mengurangi jumlah stok;
5. menyimpan histori kematian.

---

### 📜 Riwayat Penjualan

Menampilkan:

* waktu transaksi;
* nama ikan;
* jumlah ikan terjual;
* harga satuan;
* total revenue.

Data disusun dari tabel `riwayat_penjualan` dan relasinya dengan tabel `ikan`.

---

### 📋 Riwayat Kematian

Menampilkan:

* tanggal dan waktu;
* nama ikan;
* jumlah ikan mati;
* keterangan.

Data berasal dari tabel `riwayat_kematian` yang terhubung dengan `ikan`.

---

### 🔐 Autentikasi CEO

Sistem menyediakan alur:

```text
Login
  ↓
Server Verification
  ↓
Session Creation
  ↓
Dashboard
```

Pengguna yang belum memiliki session `ceo_id` tidak dapat mengakses endpoint maupun halaman yang dilindungi.

---

# 🏗️ Arsitektur Sistem

```text
┌─────────────────────────────┐
│        WEB BROWSER          │
│ HTML + CSS + Vanilla JS     │
└──────────────┬──────────────┘
               │ HTTP / JSON
               ▼
┌─────────────────────────────┐
│       FLASK BACKEND         │
│ Routing + API + Session     │
│ Validation + Business Logic │
└──────────────┬──────────────┘
               │ Psycopg
               ▼
┌─────────────────────────────┐
│        POSTGRESQL           │
│ Inventory + Sales + Death   │
│ CEO Authentication Data     │
└─────────────────────────────┘
```

### Alur autentikasi

```text
login.html
    │
    │ POST /api/auth/login
    ▼
Flask
    │
    ├── cari username aktif
    ├── verifikasi password hash
    ├── clear session lama
    └── simpan ceo_id + username
    │
    ▼
dashboard.html
```

### Alur transaksi penjualan

```text
Frontend
   │
   │ POST /api/penjualan
   ▼
Flask
   │
   ├── validasi input
   ├── SELECT ... FOR UPDATE
   ├── cek stok
   ├── hitung total harga
   ├── kurangi stok
   └── INSERT histori penjualan
   │
   ▼
PostgreSQL
```

### Alur pencatatan kematian

```text
Frontend
   │
   │ POST /api/kematian
   ▼
Flask
   │
   ├── validasi input
   ├── SELECT ... FOR UPDATE
   ├── cek stok
   ├── kurangi stok
   └── INSERT histori kematian
   │
   ▼
PostgreSQL
```

---

# 🛠️ Teknologi yang Digunakan

| Teknologi                | Fungsi dalam Project                                              |
| ------------------------ | ----------------------------------------------------------------- |
| 🐍 **Python**            | Bahasa utama backend dan business logic                           |
| 🌶️ **Flask**            | Web framework, routing, API, session, dan server-side logic       |
| 🐘 **PostgreSQL**        | Database relasional utama                                         |
| 🔌 **Psycopg 3**         | Adapter Python untuk PostgreSQL                                   |
| ⚡ **Vanilla JavaScript** | Interaksi frontend, fetch API, rendering data, form dan dashboard |
| 🌐 **HTML5**             | Struktur halaman dan interface                                    |
| 🎨 **CSS3**              | Layout, responsive design, visual interface dan animation         |
| 🔐 **Argon2**            | Hashing dan verifikasi password akun CEO                          |
| 🛡️ **Flask-Limiter**    | Pembatasan jumlah request                                         |
| 🚀 **Gunicorn**          | WSGI server untuk menjalankan aplikasi Flask                      |
| ⚙️ **python-dotenv**     | Membaca konfigurasi environment                                   |
| 🔧 **Git**               | Version control                                                   |
| ☁️ **GitHub**            | Repository dan kolaborasi source code                             |

---

# 🎨 UI & Frontend

Antarmuka menggunakan pendekatan **native HTML + CSS + Vanilla JavaScript**, tanpa React, Vue, atau framework JavaScript lainnya.

CSS utama menggunakan:

* CSS Custom Properties;
* CSS Grid;
* Flexbox;
* media queries;
* responsive layout;
* `@layer`;
* CSS animation;
* transition;
* `prefers-reduced-motion`.

Palet visual utama berorientasi pada nuansa:

```text
Teal
Blue
Green
Coral
Amber
White
Light Background
```

### Library UI eksternal

`login/login.html` menggunakan:

* Google Fonts — Inter;
* Google Fonts — DM Mono;
* Font Awesome.

`CEO.html` menggunakan:

* Google Fonts — Inter;
* Google Fonts — Space Grotesk;
* Devicon.

Library tersebut digunakan untuk kebutuhan visual interface dan iconography, bukan sebagai inti business logic sistem.

---

# 🗄️ Struktur Database

Database utama terdiri dari empat tabel.

## `ikan`

Menyimpan data persediaan ikan.

| Kolom        | Tipe          | Keterangan      |
| ------------ | ------------- | --------------- |
| `id`         | BIGINT        | Primary key     |
| `nama`       | VARCHAR(100)  | Nama ikan       |
| `foto`       | TEXT          | Path foto       |
| `kategori`   | VARCHAR(100)  | Kategori ikan   |
| `jumlah`     | INTEGER       | Jumlah stok     |
| `harga`      | NUMERIC(15,2) | Harga satuan    |
| `created_at` | TIMESTAMPTZ   | Waktu pembuatan |
| `updated_at` | TIMESTAMPTZ   | Waktu perubahan |

Constraint penting:

```text
jumlah >= 0
harga >= 0
nama NOT NULL
foto NOT NULL
kategori NOT NULL
```

---

## `riwayat_penjualan`

Menyimpan transaksi penjualan.

| Kolom          | Tipe          | Keterangan            |
| -------------- | ------------- | --------------------- |
| `id`           | BIGINT        | Primary key           |
| `ikan_id`      | BIGINT        | Foreign key ke `ikan` |
| `jumlah`       | INTEGER       | Jumlah terjual        |
| `harga_satuan` | NUMERIC(15,2) | Harga pada transaksi  |
| `total_harga`  | NUMERIC(15,2) | Total transaksi       |
| `created_at`   | TIMESTAMPTZ   | Waktu transaksi       |

---

## `riwayat_kematian`

Menyimpan kejadian mortalitas ikan.

| Kolom        | Tipe        | Keterangan               |
| ------------ | ----------- | ------------------------ |
| `id`         | BIGINT      | Primary key              |
| `ikan_id`    | BIGINT      | Foreign key ke `ikan`    |
| `jumlah`     | INTEGER     | Jumlah ikan mati         |
| `keterangan` | TEXT        | Catatan kondisi/penyebab |
| `created_at` | TIMESTAMPTZ | Waktu pencatatan         |

---

## `ceo_accounts`

Menyimpan akun autentikasi.

| Kolom           | Tipe        | Keterangan      |
| --------------- | ----------- | --------------- |
| `id`            | BIGSERIAL   | Primary key     |
| `username`      | VARCHAR(64) | Username unik   |
| `password_hash` | TEXT        | Password hash   |
| `is_active`     | BOOLEAN     | Status akun     |
| `created_at`    | TIMESTAMPTZ | Waktu pembuatan |
| `updated_at`    | TIMESTAMPTZ | Waktu perubahan |

Password tidak disimpan sebagai plaintext.

---

# 🔗 Relasi Data

```text
                 ┌──────────────────┐
                 │       ikan       │
                 │──────────────────│
                 │ id (PK)          │
                 │ nama             │
                 │ kategori         │
                 │ jumlah           │
                 │ harga            │
                 └───────┬──────────┘
                         │
               ┌─────────┴─────────┐
               │                   │
               ▼                   ▼
┌──────────────────────┐  ┌──────────────────────┐
│ riwayat_penjualan    │  │ riwayat_kematian     │
│──────────────────────│  │──────────────────────│
│ id                   │  │ id                   │
│ ikan_id (FK)         │  │ ikan_id (FK)         │
│ jumlah               │  │ jumlah               │
│ harga_satuan         │  │ keterangan           │
│ total_harga          │  │ created_at           │
│ created_at           │  │                      │
└──────────────────────┘  └──────────────────────┘
```

Foreign key menggunakan:

```sql
ON DELETE RESTRICT
```

Artinya data ikan tidak dapat dihapus ketika masih memiliki histori penjualan atau histori kematian yang terkait.

---

# 🔌 API Reference

Semua endpoint berikut adalah endpoint yang benar-benar didefinisikan pada `app.py`.

| Method   | Endpoint           | Auth    | Fungsi                             |
| -------- | ------------------ | ------- | ---------------------------------- |
| `GET`    | `/api/health`      | No      | Health check aplikasi dan database |
| `GET`    | `/api/ikan`        | Yes     | Mengambil seluruh data ikan        |
| `GET`    | `/api/ikan/<id>`   | Yes     | Mengambil satu data ikan           |
| `POST`   | `/api/ikan`        | Yes     | Menambah ikan                      |
| `PUT`    | `/api/ikan/<id>`   | Yes     | Memperbarui ikan                   |
| `PUT`    | `/api/ikan`        | Yes     | Bulk synchronisation data ikan     |
| `DELETE` | `/api/ikan/<id>`   | Yes     | Menghapus ikan                     |
| `GET`    | `/api/kematian`    | Yes     | Mengambil histori kematian         |
| `POST`   | `/api/kematian`    | Yes     | Mencatat kematian                  |
| `GET`    | `/api/penjualan`   | Yes     | Mengambil histori penjualan        |
| `POST`   | `/api/penjualan`   | Yes     | Mencatat transaksi penjualan       |
| `POST`   | `/api/auth/login`  | No      | Autentikasi CEO                    |
| `GET`    | `/api/auth/me`     | Session | Memeriksa sesi login               |
| `POST`   | `/api/auth/logout` | Session | Menghapus sesi                     |

Login dibatasi secara khusus:

```text
5 request / minute
```

Aplikasi juga memiliki default rate limit:

```text
300 request / minute
```

---

# 🔐 Security Implementation

Project menerapkan beberapa lapisan pengamanan pada sisi aplikasi.

### Password Hashing

Akun CEO tidak menyimpan password plaintext.

`create_ceo.py` menggunakan:

```python
PasswordHasher()
```

untuk menghasilkan password hash sebelum dimasukkan ke database.

Pendekatan ini sesuai dengan rekomendasi OWASP bahwa password tidak seharusnya disimpan dalam plaintext dan sebaiknya menggunakan password hashing yang adaptif seperti Argon2.

---

### Session Authentication

Akses halaman dan API operasional dikontrol melalui session:

```python
session["ceo_id"]
session["ceo_username"]
```

Decorator:

```python
@auth_required
```

digunakan pada endpoint yang membutuhkan login.

---

### Session Cookie

Aplikasi mengaktifkan:

```text
HttpOnly = True
SameSite = Lax
Secure = configurable
```

Nilai `SESSION_COOKIE_SECURE` dapat dikendalikan melalui environment.

Untuk deployment HTTPS, konfigurasi sebaiknya menggunakan:

```text
SESSION_COOKIE_SECURE=true
```

---

### Secret Key

Secret Flask diperoleh dari:

```text
FLASK_SECRET_KEY
```

Jika variabel tersebut tidak tersedia, aplikasi membuat secret sementara menggunakan `secrets.token_hex(32)`.

Untuk deployment, secret key sebaiknya ditentukan secara eksplisit melalui environment agar session tidak berubah ketika process restart.

---

### Environment Variables

Konfigurasi database tidak ditulis langsung dalam source code.

Aplikasi mendukung:

```text
DATABASE_URL
```

atau:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

File `.env` dimasukkan ke `.gitignore`.

---

### SQL Parameterisation

Query database menggunakan parameter binding Psycopg:

```python
conn.execute(
    "... WHERE id = %s",
    (fish_id,)
)
```

Pendekatan tersebut mencegah penyusunan query SQL menggunakan string concatenation dari input user.

---

### Transaction & Row Locking

Operasi penjualan dan kematian menggunakan transaksi database dan:

```sql
FOR UPDATE
```

untuk mengunci row ikan selama proses perubahan stok.

Tujuannya adalah menjaga konsistensi ketika stok dibaca, diperiksa, dan dikurangi dalam satu transaksi.

---

### Request Size Limit

Aplikasi menetapkan:

```text
MAX_CONTENT_LENGTH = 64 KiB
```

untuk membatasi ukuran request.

---

### HTTP Security Headers

Aplikasi menambahkan:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

API juga menggunakan:

```text
Cache-Control: no-store
```

---

### Rate Limiting

Flask-Limiter digunakan dengan:

```text
default = 300/minute
login = 5/minute
```

Default storage saat ini:

```text
memory://
```

Konfigurasi storage dapat diubah melalui:

```text
RATELIMIT_STORAGE_URI
```

Untuk deployment multi-worker, shared storage lebih sesuai daripada in-memory storage.

---

# 📊 Dataset Awal

`database/seed.sql` menyediakan dataset contoh untuk kebutuhan pengembangan dan pengujian.

Hasil perhitungan dari dataset seed saat ini:

| Data                                            |             Nilai |
| ----------------------------------------------- | ----------------: |
| Jenis data ikan                                 |            **31** |
| Kategori                                        |            **11** |
| Total stok awal                                 |    **4.280 ekor** |
| Nilai nominal stok berdasarkan `jumlah × harga` | **Rp162.660.000** |

Nilai tersebut berasal dari **dataset contoh di repository**, bukan hasil audit pasar atau survei harga ikan aktual.

Kategori yang terdapat dalam dataset meliputi antara lain:

```text
Predator
Hias Kecil
Cupang
Pembersih
Molly
Koki
Koi
Channa
Crustacea
Hias
Hias Besar
```

---

# 📁 Struktur Repository

```text
CAPSTONE_PROJECT_KELOMPOK_B/
│
├── app.py
├── CEO.html
├── dashboard.html
├── create_ceo.py
├── ceo_auth.sql
├── gunicorn.conf.py
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── images/
│   │   ├── logo.png
│   │   └── *.jpg
│   └── readme/
│       ├── login.png
│       ├── dasboard.png
│       └── profile.png
│
├── css/
│   └── style.css
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── permissions.sql
│
├── docs/
│   ├── Karil_Sumber_Aquarium_Kelompok_B.docx
│   └── Sumber_Aquarium_PGK_Presentation.pptx
│
├── js/
│   ├── app.js
│   └── auth.js
│
├── login/
│   └── login.html
│
└── modules/
    ├── catat-kematian/
    │   └── catatankematian.html
    │
    ├── catat-penjualan/
    │   └── catatanpenjualan.html
    │
    ├── riwayat-kematian/
    │   └── riwayatkematian.html
    │
    ├── riwayat-penjualan/
    │   └── riwayatpenjualan.html
    │
    ├── stok-ikan/
    │   └── stokikan.html
    │
    └── tambah-ikan/
        └── tambahikan.html
```

---

# 🖥️ Halaman Aplikasi

### Login

```text
/
 /login
 /login.html
```

Mengarahkan pengguna ke halaman autentikasi CEO apabila belum memiliki session aktif.

### Dashboard

```text
/dashboard.html
```

Pusat ringkasan operasional.

### Profile

```text
/CEO.html
```

Halaman profil project dan anggota kelompok.

### Modul

```text
/modules/stok-ikan/stokikan.html
/modules/tambah-ikan/tambahikan.html
/modules/catat-penjualan/catatanpenjualan.html
/modules/riwayat-penjualan/riwayatpenjualan.html
/modules/catat-kematian/catatankematian.html
/modules/riwayat-kematian/riwayatkematian.html
```

---


# 🖼️ Interface Preview

## 🔐 Login

![Login Sumber Aquarium](assets/readme/login.png)

## 📊 Dashboard

![Dashboard Sumber Aquarium](assets/readme/dasboard.png)

## 👨‍💼 CEO Dashboard Preview

[![CEO Dashboard Preview](assets/readme/ceo-preview.gif)](ceo.mp4)

## 🎬 System Preview

[![System Preview](assets/readme/preview.gif)](previews.mp4)

------

# 📦 Dependencies

`requirements.txt` saat ini menggunakan:

```text
Flask>=3.1,<4
psycopg[binary]>=3.2,<4
python-dotenv>=1.0,<2
argon2-cffi>=23.1,<26
Flask-Limiter>=3.5,<5
gunicorn==26.2.0
```

---

# 🚀 Instalasi Lokal

## 1. Clone repository

```bash
git clone https://github.com/Zzzzzzzpeng/CAPSTONE_PROJECT_KELOMPOK_B.git
cd CAPSTONE_PROJECT_KELOMPOK_B
```

---

## 2. Buat virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Buat konfigurasi environment

Buat file:

```text
.env
```

Contoh konfigurasi:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@127.0.0.1:5432/DBNAME

FLASK_SECRET_KEY=GANTI_DENGAN_SECRET_RANDOM_YANG_PANJANG

SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=false

RATELIMIT_STORAGE_URI=memory://

HOST=127.0.0.1
PORT=5000
FLASK_DEBUG=0
LOG_LEVEL=INFO
```

Jangan memasukkan credential asli ke repository.

---

# 🐘 Persiapan PostgreSQL

Buat database sesuai kebutuhan environment lokal.

Kemudian jalankan schema:

```bash
psql "$DATABASE_URL" -f database/schema.sql
```

Buat tabel autentikasi:

```bash
psql "$DATABASE_URL" -f ceo_auth.sql
```

Masukkan dataset awal:

```bash
psql "$DATABASE_URL" -f database/seed.sql
```

---

## Permissions

File:

```text
database/permissions.sql
```

saat ini menggunakan PostgreSQL role:

```text
peng
```

Karena itu file tersebut bersifat **environment-specific**.

Jangan menjalankannya secara buta pada database yang menggunakan role berbeda.

Jika role yang digunakan memang `peng`:

```bash
psql "$DATABASE_URL" -f database/permissions.sql
```

---

# 👤 Membuat Akun CEO

Gunakan:

```bash
python create_ceo.py
```

Script akan meminta:

```text
CEO username:
CEO password:
Repeat password:
```

Password kemudian di-hash menggunakan Argon2 sebelum disimpan ke:

```text
ceo_accounts.password_hash
```

---

# ▶️ Menjalankan Aplikasi

### Development

```bash
python app.py
```

Default:

```text
127.0.0.1:5000
```

### Gunicorn

Project menyediakan:

```text
gunicorn.conf.py
```

Jalankan:

```bash
gunicorn -c gunicorn.conf.py app:app
```

Konfigurasi repository saat ini menggunakan:

```text
bind = 127.0.0.1:5000
workers = 2
worker_class = sync
timeout = 120
graceful_timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
worker_tmp_dir = /dev/shm
```

Konfigurasi tersebut menjalankan Flask melalui Gunicorn pada interface localhost.

---

# 📝 Dokumentasi Akademik

Repository juga menyimpan artefak akademik project:

```text
docs/Karil_Sumber_Aquarium_Kelompok_B.docx
docs/Sumber_Aquarium_PGK_Presentation.pptx
```

Dokumen tersebut menjadi bagian dari dokumentasi dan penyampaian hasil Capstone Project kelompok.

---

# 🧪 Status Project

```text
Project Type : Academic Capstone Project
Scope        : Information System
Architecture : Client / Server
Frontend     : HTML + CSS + Vanilla JavaScript
Backend      : Python + Flask
Database     : PostgreSQL
Authentication: Session + Argon2
Deployment   : Gunicorn
Versioning   : Git + GitHub
```

Project ini merupakan **project akademik dan prototype sistem**, sehingga konfigurasi dan beberapa aspek deployment masih perlu disesuaikan sebelum digunakan sebagai aplikasi produksi publik.

---

# ⚠️ Production Hardening

Sebelum deployment publik, beberapa konfigurasi perlu diperhatikan:

### Secret

Gunakan `FLASK_SECRET_KEY` yang eksplisit dan random.

### HTTPS

Aktifkan:

```env
SESSION_COOKIE_SECURE=true
```

ketika aplikasi dijalankan di HTTPS.

### Rate Limit Storage

Default:

```text
memory://
```

cukup untuk development sederhana, tetapi deployment multi-worker sebaiknya menggunakan shared storage yang sesuai.

### CSRF

Repository saat ini menggunakan session cookie untuk autentikasi, tetapi belum menunjukkan implementasi CSRF token pada endpoint perubahan data. Perlindungan CSRF perlu ditambahkan sebelum deployment publik.

### Automated Testing

Tidak terdapat direktori test automation pada struktur repository saat ini. Automated test untuk API, transaksi stok, authentication, dan permission dapat ditambahkan sebagai pengembangan lanjutan.

---

# 🔭 Pengembangan Selanjutnya

Beberapa area yang dapat dikembangkan:

```text
Database
 ├── audit trail
 ├── role-based access control
 └── reporting

Backend
 ├── automated testing
 ├── API versioning
 ├── CSRF protection
 └── production observability

Frontend
 ├── filtering lanjutan
 ├── pagination
 ├── visual analytics
 └── improved form validation

Deployment
 ├── HTTPS
 ├── reverse proxy
 ├── shared rate-limit storage
 └── production database configuration
```

---

# 📚 Referensi 

Flask. (n.d.). *Quickstart*. Pallets Projects.
https://flask.palletsprojects.com/en/stable/quickstart/

Flask-Limiter. (n.d.). *Flask-Limiter documentation*.
https://flask-limiter.readthedocs.io/en/stable/

Gunicorn. (n.d.). *Gunicorn documentation*.
https://docs.gunicorn.org/

OWASP Foundation. (n.d.). *Password storage cheat sheet*.
https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

PostgreSQL Global Development Group. (n.d.). *About PostgreSQL*.
https://www.postgresql.org/about/

Psycopg. (n.d.). *Psycopg 3 documentation*.
https://www.psycopg.org/psycopg3/docs/

Universitas Terbuka. (2025, February 18). *Mengenal Capstone Project mata kuliah STSI4401*. Program Studi S1 Sistem Informasi, Fakultas Sains dan Teknologi, Universitas Terbuka.
https://si-fst.ut.ac.id/2025/02/18/mengenal-capstone-project-mata-kuliah-stsi4401/

---

# 📌 Ringkasan

**Sumber Aquarium PGK** adalah implementasi sistem informasi berbasis web yang mengintegrasikan:

```text
HTML
   +
CSS
   +
Vanilla JavaScript
   +
Python / Flask
   +
Psycopg
   +
PostgreSQL
   +
Argon2
   +
Flask-Limiter
   +
Gunicorn
```

Seluruh komponen tersebut membentuk satu alur sistem untuk:

```text
Authentication
      ↓
Dashboard
      ↓
Inventory
      ↓
Sales
      ↓
Fish Mortality
      ↓
Operational History
      ↓
PostgreSQL
```

Project ini merupakan hasil kerja akademik **Kelompok B, Program Studi S1 Sistem Informasi, Universitas Terbuka**, dengan pembagian kontribusi pada fondasi sistem dan data, dokumentasi, komunikasi visual, serta full-stack dan integrasi sistem.
