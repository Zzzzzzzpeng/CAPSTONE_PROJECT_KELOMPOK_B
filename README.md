 
# 🐟 Sumber Aquarium PGK

### Sistem Informasi Pengelolaan Toko Ikan Hias

**Capstone Project — Program Studi S1 Sistem Informasi, Universitas Terbuka**

> Satu sistem untuk mengelola persediaan, penjualan, mortalitas, dan histori operasional toko ikan hias.

Sumber Aquarium PGK adalah aplikasi sistem informasi berbasis web yang dikembangkan sebagai **Capstone Project Kelompok B Program Studi S1 Sistem Informasi Universitas Terbuka**.

Sistem ini dirancang untuk membantu pengelolaan data operasional toko ikan hias melalui satu aplikasi yang mengintegrasikan:

* data persediaan ikan;
* kategori dan harga ikan;
* pencatatan penjualan;
* pencatatan kematian ikan;
* histori penjualan;
* histori mortalitas;
* dashboard operasional;
* autentikasi pengguna;
* database relasional PostgreSQL.

Aplikasi menggunakan arsitektur client-server sederhana dengan **HTML, CSS, Vanilla JavaScript, Python/Flask, Psycopg 3, dan PostgreSQL**.

---

# 🎓 Tentang Project

Sumber Aquarium PGK dikembangkan dalam konteks pembelajaran Capstone Project pada Program Studi S1 Sistem Informasi.

Project ini berfokus pada penerapan kemampuan perancangan dan implementasi sistem informasi, bukan pada klaim kebaruan teknologi.

Implementasi mencakup beberapa lapisan sistem:

```text
User Interface
      ↓
Vanilla JavaScript
      ↓
HTTP / JSON API
      ↓
Flask Backend
      ↓
Psycopg 3
      ↓
PostgreSQL
```

Sistem dibuat untuk menunjukkan bagaimana proses operasional toko ikan hias dapat dimodelkan menjadi data dan proses digital yang saling terintegrasi.

---

# 👥 Kelompok B

**Program Studi S1 Sistem Informasi
Universitas Terbuka**

| Anggota                  | NIM         | Kontribusi                                                                                    |
| ------------------------ | ----------- | --------------------------------------------------------------------------------------------- |
| **DIMAS**                | `050039851` | Fondasi sistem dan data, termasuk kontribusi awal HTML, CSS, JavaScript, serta data pendukung |
| **DHEA HANDANUR AINI**   | `050417407` | Dokumentasi dan proposal proyek                                                               |
| **KAMALUDIN**            | `050595262` | Komunikasi visual, presentasi, dan materi penyampaian proyek                                  |
| **MUHAMAD ARPAN KURNIA** | `051102736` | Full-stack integration, API, database, autentikasi, keamanan aplikasi, dan deployment         |

> Pembagian kontribusi di atas mengikuti dokumentasi project pada repository.

---

# 🎯 Tujuan Sistem

Sumber Aquarium PGK dikembangkan untuk menyediakan pengelolaan informasi operasional yang lebih terstruktur.

Tujuan utama sistem:

1. Mengelola data ikan dan stok.
2. Mencatat harga serta kategori ikan.
3. Mencatat transaksi penjualan.
4. Mengurangi stok secara otomatis ketika terjadi penjualan.
5. Mencatat kejadian kematian ikan.
6. Mengurangi stok berdasarkan pencatatan mortalitas.
7. Menyimpan histori penjualan dan kematian.
8. Menampilkan ringkasan operasional melalui dashboard.
9. Membatasi akses terhadap data melalui autentikasi session.
10. Menyimpan data secara terpusat pada PostgreSQL.

---

# 🧩 Fitur Utama

## 📊 Dashboard

Dashboard mengambil data dari tiga endpoint utama:

```text
GET /api/ikan
GET /api/penjualan
GET /api/kematian
```

Data kemudian dihitung dan ditampilkan pada sisi frontend.

Informasi yang ditampilkan meliputi:

* total stok ikan;
* jumlah jenis ikan;
* jumlah transaksi penjualan;
* jumlah kejadian kematian;
* jumlah jenis ikan dengan stok ≤ 10;
* akumulasi nilai transaksi penjualan;
* lima transaksi penjualan terakhir;
* lima kejadian kematian terakhir;
* username pengguna yang sedang login;
* waktu sinkronisasi dashboard.

Perhitungan total stok dilakukan berdasarkan jumlah seluruh `jumlah` pada data ikan.

Batas stok perhatian pada dashboard saat ini adalah:

```text
jumlah <= 10
```

---

## 🐟 Manajemen Stok

Modul stok menyediakan informasi:

* ID ikan;
* nama ikan;
* kategori;
* jumlah stok;
* harga satuan;
* foto ikan;
* pencarian data;
* pengeditan data;
* penghapusan data.

Data bersumber dari tabel:

```text
ikan
```

Penghapusan dibatasi oleh foreign key database sehingga ikan yang sudah memiliki histori penjualan atau kematian tidak dapat dihapus begitu saja.

---

## ➕ Tambah Ikan

Data ikan baru dapat ditambahkan melalui modul tambah ikan.

Field utama:

```text
Nama ikan
Kategori
Stok awal
Harga
```

Data dikirim ke backend menggunakan:

```http
POST /api/ikan
```

Backend melakukan validasi terhadap:

* nama;
* kategori;
* jumlah;
* harga;
* path foto.

Jika foto tidak diberikan, sistem menggunakan:

```text
/assets/images/logo.png
```

---

## ✏️ Edit Data Ikan

Data ikan dapat diperbarui melalui:

```http
PUT /api/ikan/<id>
```

Backend memperbarui:

```text
nama
foto
kategori
jumlah
harga
```

Database juga memiliki trigger untuk memperbarui `updated_at` ketika data ikan berubah.

---

## 🛒 Pencatatan Penjualan

Pencatatan penjualan menerima:

```text
ikan_id
jumlah
```

Proses pada backend:

```text
Request
   ↓
Validasi input
   ↓
SELECT ikan ... FOR UPDATE
   ↓
Periksa keberadaan ikan
   ↓
Periksa kecukupan stok
   ↓
Hitung total harga
   ↓
Kurangi stok
   ↓
Simpan histori penjualan
   ↓
Commit transaction
```

Total transaksi dihitung menggunakan:

```text
harga ikan × jumlah terjual
```

Histori disimpan pada:

```text
riwayat_penjualan
```

Endpoint:

```http
GET  /api/penjualan
POST /api/penjualan
```

---

## ⚠️ Pencatatan Mortalitas

Modul mortalitas digunakan untuk mencatat ikan yang mengalami kematian.

Input:

```text
ikan
jumlah ikan mati
keterangan
```

Alurnya:

```text
Request
   ↓
Validasi input
   ↓
SELECT ikan ... FOR UPDATE
   ↓
Periksa stok
   ↓
Kurangi stok
   ↓
Simpan histori kematian
   ↓
Commit transaction
```

Endpoint:

```http
GET  /api/kematian
POST /api/kematian
```

Histori disimpan pada:

```text
riwayat_kematian
```

Keterangan mortalitas dapat digunakan untuk mencatat kondisi atau penyebab yang diketahui oleh pengguna.

---

# 📜 Histori Penjualan

Halaman histori penjualan menampilkan:

* waktu transaksi;
* nama ikan;
* jumlah;
* harga satuan;
* total harga.

Data diambil dari relasi:

```text
riwayat_penjualan
        ↓
      ikan
```

Data transaksi diurutkan dari transaksi terbaru.

---

# 📋 Histori Mortalitas

Halaman histori mortalitas menampilkan:

* waktu kejadian;
* nama ikan;
* jumlah ikan mati;
* keterangan.

Halaman juga menyediakan ringkasan:

* jumlah kejadian;
* total ikan yang mati;
* jumlah jenis ikan yang terdampak.

Pencarian dapat dilakukan berdasarkan:

```text
Nama ikan
Keterangan
```

---

# 🔐 Autentikasi

Sistem menggunakan autentikasi berbasis session.

Alurnya:

```text
Login
  ↓
POST /api/auth/login
  ↓
Cari username aktif
  ↓
Verifikasi password hash
  ↓
Session dibuat
  ↓
Dashboard
```

Session menyimpan:

```python
session["ceo_id"]
session["ceo_username"]
```

Endpoint autentikasi:

```http
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

Endpoint operasional menggunakan decorator:

```python
@auth_required
```

sehingga hanya session yang valid yang dapat mengakses data operasional.

---

# 🏗️ Arsitektur Sistem

```text
┌─────────────────────────────────┐
│          WEB BROWSER            │
│                                 │
│ HTML5 + CSS3 + Vanilla JS       │
└───────────────┬─────────────────┘
                │
                │ HTTP / JSON
                ▼
┌─────────────────────────────────┐
│         FLASK BACKEND           │
│                                 │
│ Routing                         │
│ API                             │
│ Authentication                  │
│ Validation                      │
│ Business Logic                  │
│ Session Management              │
└───────────────┬─────────────────┘
                │
                │ Psycopg 3
                ▼
┌─────────────────────────────────┐
│          POSTGRESQL             │
│                                 │
│ Inventory                       │
│ Sales History                   │
│ Mortality History               │
│ CEO Accounts                    │
└─────────────────────────────────┘
```

---

# 🛠️ Technology Stack

| Teknologi              | Penggunaan                           |
| ---------------------- | ------------------------------------ |
| **Python**             | Backend dan business logic           |
| **Flask**              | Web framework, routing, API, session |
| **PostgreSQL**         | Database relasional                  |
| **Psycopg 3**          | Koneksi Python ke PostgreSQL         |
| **Vanilla JavaScript** | Interaksi frontend dan API           |
| **HTML5**              | Struktur halaman                     |
| **CSS3**               | Layout, responsive design, animation |
| **Argon2**             | Password hashing dan verification    |
| **Flask-Limiter**      | Rate limiting                        |
| **Gunicorn**           | WSGI server                          |
| **python-dotenv**      | Environment configuration            |
| **Git**                | Version control                      |
| **GitHub**             | Repository dan kolaborasi            |

---

# 🎨 UI / UX

Frontend menggunakan:

```text
HTML5
CSS3
Vanilla JavaScript
```

Tidak menggunakan:

```text
React
Vue
Angular
Next.js
Bootstrap
Tailwind CSS
```

Styling utama menggunakan CSS native dengan:

* CSS Custom Properties;
* CSS Grid;
* Flexbox;
* media queries;
* responsive layout;
* CSS animation;
* transitions;
* `prefers-reduced-motion`.

Global stylesheet menggunakan font:

```text
Inter
Space Grotesk
```

Halaman CEO juga menggunakan:

```text
JetBrains Mono
Space Grotesk
```

Repository menggunakan **Devicon** untuk beberapa icon teknologi pada halaman profil/CEO.

---

# 🖥️ Halaman Aplikasi

Struktur utama aplikasi:

```text
/
├── Login
│
├── Dashboard
│
├── Stok Ikan
│
├── Tambah Ikan
│
├── Catat Penjualan
│
├── Riwayat Penjualan
│
├── Catat Kematian
│
├── Riwayat Kematian
│
└── Profil / CEO
```

File utama:

```text
login/login.html
dashboard.html
CEO.html

modules/
├── stok-ikan/stokikan.html
├── tambah-ikan/tambahikan.html
├── catat-penjualan/catatanpenjualan.html
├── riwayat-penjualan/riwayatpenjualan.html
├── catat-kematian/catatankematian.html
└── riwayat-kematian/riwayatkematian.html
```

---

# 🗄️ Database

Database menggunakan PostgreSQL.

Struktur utama terdiri dari:

```text
ikan
riwayat_penjualan
riwayat_kematian
ceo_accounts
```

## Tabel `ikan`

Menyimpan data persediaan.

| Kolom        | Tipe          | Keterangan      |
| ------------ | ------------- | --------------- |
| `id`         | BIGINT        | Primary key     |
| `nama`       | VARCHAR(100)  | Nama ikan       |
| `foto`       | TEXT          | Path foto       |
| `kategori`   | VARCHAR(100)  | Kategori        |
| `jumlah`     | INTEGER       | Jumlah stok     |
| `harga`      | NUMERIC(15,2) | Harga satuan    |
| `created_at` | TIMESTAMPTZ   | Waktu pembuatan |
| `updated_at` | TIMESTAMPTZ   | Waktu perubahan |

Constraint:

```text
jumlah >= 0
harga >= 0
nama NOT NULL
foto NOT NULL
kategori NOT NULL
```

---

## Tabel `riwayat_penjualan`

Menyimpan transaksi penjualan.

| Kolom          | Tipe          | Keterangan             |
| -------------- | ------------- | ---------------------- |
| `id`           | BIGINT        | Primary key            |
| `ikan_id`      | BIGINT        | Foreign key            |
| `jumlah`       | INTEGER       | Jumlah terjual         |
| `harga_satuan` | NUMERIC(15,2) | Harga ketika transaksi |
| `total_harga`  | NUMERIC(15,2) | Total transaksi        |
| `created_at`   | TIMESTAMPTZ   | Waktu transaksi        |

---

## Tabel `riwayat_kematian`

Menyimpan kejadian mortalitas.

| Kolom        | Tipe        | Keterangan         |
| ------------ | ----------- | ------------------ |
| `id`         | BIGINT      | Primary key        |
| `ikan_id`    | BIGINT      | Foreign key        |
| `jumlah`     | INTEGER     | Jumlah ikan mati   |
| `keterangan` | TEXT        | Kondisi/keterangan |
| `created_at` | TIMESTAMPTZ | Waktu pencatatan   |

---

## Tabel `ceo_accounts`

Menyimpan data autentikasi.

| Kolom           | Tipe        | Keterangan      |
| --------------- | ----------- | --------------- |
| `id`            | BIGSERIAL   | Primary key     |
| `username`      | VARCHAR(64) | Username unik   |
| `password_hash` | TEXT        | Password hash   |
| `is_active`     | BOOLEAN     | Status akun     |
| `created_at`    | TIMESTAMPTZ | Waktu pembuatan |
| `updated_at`    | TIMESTAMPTZ | Waktu perubahan |

Password tidak disimpan dalam bentuk plaintext.

---

# 🔗 Relasi Database

```text
                    ┌───────────────┐
                    │     ikan      │
                    │───────────────│
                    │ id PK         │
                    │ nama          │
                    │ kategori      │
                    │ jumlah        │
                    │ harga         │
                    └───────┬───────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
       ┌──────────────────┐   ┌──────────────────┐
       │ riwayat_penjualan│   │ riwayat_kematian │
       │──────────────────│   │──────────────────│
       │ ikan_id FK       │   │ ikan_id FK       │
       │ jumlah           │   │ jumlah           │
       │ harga_satuan     │   │ keterangan       │
       │ total_harga      │   │ created_at       │
       └──────────────────┘   └──────────────────┘
```

Foreign key menggunakan:

```sql
ON DELETE RESTRICT
```

Artinya data ikan yang masih memiliki histori terkait tidak dapat dihapus.

Database juga menggunakan index pada:

```text
riwayat_kematian.ikan_id
riwayat_kematian.created_at
riwayat_penjualan.ikan_id
riwayat_penjualan.created_at
```

---

# 🔌 API Reference

Semua endpoint utama didefinisikan pada `app.py`.

| Method | Endpoint           | Auth    | Fungsi             |
| ------ | ------------------ | ------- | ------------------ |
| GET    | `/api/health`      | Tidak   | Health check       |
| GET    | `/api/ikan`        | Ya      | Seluruh data ikan  |
| GET    | `/api/ikan/<id>`   | Ya      | Detail ikan        |
| POST   | `/api/ikan`        | Ya      | Tambah ikan        |
| PUT    | `/api/ikan/<id>`   | Ya      | Edit ikan          |
| DELETE | `/api/ikan/<id>`   | Ya      | Hapus ikan         |
| GET    | `/api/kematian`    | Ya      | Histori kematian   |
| POST   | `/api/kematian`    | Ya      | Catat kematian     |
| GET    | `/api/penjualan`   | Ya      | Histori penjualan  |
| POST   | `/api/penjualan`   | Ya      | Catat penjualan    |
| POST   | `/api/auth/login`  | Tidak   | Login              |
| GET    | `/api/auth/me`     | Session | Status autentikasi |
| POST   | `/api/auth/logout` | Session | Logout             |

---

# 🔒 Security Implementation

Project menerapkan beberapa mekanisme keamanan pada level aplikasi dan database.

## Password Hashing

`create_ceo.py` menggunakan:

```python
PasswordHasher()
```

Password disimpan sebagai hash pada:

```text
ceo_accounts.password_hash
```

Sistem tidak menyimpan password plaintext.

---

## Session Authentication

Akses endpoint operasional membutuhkan session:

```python
session["ceo_id"]
session["ceo_username"]
```

Decorator:

```python
@auth_required
```

digunakan untuk membatasi endpoint.

---

## Session Cookie

Konfigurasi aplikasi:

```text
HttpOnly = True
SameSite = configurable
Secure = configurable
```

Environment yang tersedia:

```text
SESSION_COOKIE_SAMESITE
SESSION_COOKIE_SECURE
```

Untuk deployment HTTPS, `SESSION_COOKIE_SECURE` sebaiknya diaktifkan.

---

## Secret Key

Flask menggunakan:

```text
FLASK_SECRET_KEY
```

Jika tidak tersedia, aplikasi membuat secret sementara menggunakan:

```python
secrets.token_hex(32)
```

Untuk deployment, secret sebaiknya diberikan secara eksplisit melalui environment.

---

## SQL Parameterization

Query PostgreSQL menggunakan parameter binding Psycopg.

Contoh:

```python
conn.execute(
    "... WHERE id = %s",
    (fish_id,)
)
```

Input pengguna tidak digabungkan langsung ke string SQL.

---

## Transaction dan Row Locking

Transaksi penjualan dan mortalitas menggunakan:

```sql
SELECT ...
FOR UPDATE
```

Tujuannya untuk mengunci row ikan selama proses pemeriksaan dan perubahan stok.

Dengan demikian alurnya menjadi:

```text
Read stock
   ↓
Lock row
   ↓
Validate stock
   ↓
Update stock
   ↓
Insert history
   ↓
Commit
```

---

## Request Size Limit

Flask dikonfigurasi dengan:

```python
MAX_CONTENT_LENGTH = 64 * 1024
```

atau:

```text
64 KiB
```

Request yang melebihi batas akan ditolak pada level Flask.

---

## HTTP Security Headers

Aplikasi menambahkan:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

Untuk endpoint API:

```text
Cache-Control: no-store
```

---

## Rate Limiting

Flask-Limiter digunakan dengan konfigurasi:

```text
Default:
300 request / minute

Login:
5 request / minute
```

Storage default:

```text
memory://
```

Konfigurasi storage dapat diganti melalui:

```text
RATELIMIT_STORAGE_URI
```

Untuk deployment multi-worker, shared storage perlu dipertimbangkan.

---

# 📊 Dataset Seed

Repository menyediakan dataset contoh melalui:

```text
database/seed.sql
```

Dataset tersebut digunakan untuk pengembangan dan demonstrasi sistem.

Hasil perhitungan dari seed saat ini:

| Informasi          |             Nilai |
| ------------------ | ----------------: |
| Jenis ikan         |            **31** |
| Kategori           |            **11** |
| Total stok         |    **4.280 ekor** |
| Nilai nominal stok | **Rp162.660.000** |

Nilai nominal dihitung dari:

```text
jumlah × harga
```

Nilai tersebut merupakan **dataset contoh repository**, bukan hasil survei harga pasar atau audit bisnis aktual.

Kategori yang terdapat dalam dataset:

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

# 📦 Dependencies

`requirements.txt` saat ini:

```text
Flask>=3.1,<4
psycopg[binary]>=3.2,<4
python-dotenv>=1.0,<2
argon2-cffi>=23.1,<26
Flask-Limiter>=3.5,<5
gunicorn==26.2.0
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
│   ├── ceo.mp4
│   ├── images/
│   │   ├── logo.png
│   │   ├── *.jpg
│   │   └── profile images
│   │
│   └── readme/
│       ├── login.png
│       ├── dashboard.png
│       ├── stokikan.png
│       ├── tambahikan.png
│       ├── catatanpenjualan.png
│       ├── riwayatpenjualan.png
│       ├── catatankematian.png
│       └── riwayatkematian.png
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
    ├── catat-penjualan/
    ├── riwayat-kematian/
    ├── riwayat-penjualan/
    ├── stok-ikan/
    └── tambah-ikan/
```

---

# 🚀 Instalasi Lokal

## 1. Clone Repository

```bash
git clone https://github.com/Zzzzzzzpeng/CAPSTONE_PROJECT_KELOMPOK_B.git
cd CAPSTONE_PROJECT_KELOMPOK_B
```

## 2. Buat Virtual Environment

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Configuration

Buat file:

```text
.env
```

Contoh:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@127.0.0.1:5432/DBNAME

FLASK_SECRET_KEY=GANTI_DENGAN_SECRET_RANDOM_YANG_PANJANG ( python -c "import secrets; print(secrets.token_urlsafe(64))")

SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=false

RATELIMIT_STORAGE_URI=memory://

HOST=127.0.0.1
PORT=5000
FLASK_DEBUG=0
LOG_LEVEL=INFO
```

Alternatif konfigurasi database juga tersedia:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

Jangan memasukkan credential database atau secret asli ke repository.

---

# 🐘 Persiapan PostgreSQL

Buat database PostgreSQL sesuai environment lokal.

Kemudian jalankan:

```bash
psql "$DATABASE_URL" -f database/schema.sql
```

Buat tabel autentikasi:

```bash
psql "$DATABASE_URL" -f ceo_auth.sql
```

Masukkan dataset:

```bash
psql "$DATABASE_URL" -f database/seed.sql
```

---

# ⚠️ Permissions

File:

```text
database/permissions.sql
```

menggunakan role PostgreSQL:

```text
peng
```

File tersebut bersifat **environment-specific**.

Jangan menjalankannya tanpa menyesuaikan role database.

Jika role database memang bernama `peng`:

```bash
psql "$DATABASE_URL" -f database/permissions.sql
```

---

# 👤 Membuat Akun CEO

Gunakan:

```bash
python create_ceo.py
```

Script meminta:

```text
CEO username:
CEO password:
Repeat password:
```

Password kemudian di-hash sebelum disimpan ke:

```text
ceo_accounts.password_hash
```

---

# ▶️ Menjalankan Aplikasi

## Development

```bash
python app.py
```

Default:

```text
127.0.0.1:5000
```

Kemudian buka:

```text
http://127.0.0.1:5000
```

## Gunicorn

Repository menyediakan:

```text
gunicorn.conf.py
```

Jalankan:

```bash
gunicorn -c gunicorn.conf.py app:app
```

Konfigurasi saat ini:

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

Konfigurasi tersebut merupakan konfigurasi repository saat ini dan bukan klaim bahwa konfigurasi tersebut otomatis sesuai untuk seluruh deployment produksi.

---

# 🖼️ Interface Preview

## Login

![Login](assets/readme/login.png)

## Dashboard

![Dashboard](assets/readme/dashboard.png)

## Stok Ikan

![Stok Ikan](assets/readme/stokikan.png)

## Tambah Ikan

![Tambah Ikan](assets/readme/tambahikan.png)

## Catat Penjualan

![Catat Penjualan](assets/readme/catatanpenjualan.png)

## Riwayat Penjualan

![Riwayat Penjualan](assets/readme/riwayatpenjualan.png)

## Catat Kematian

![Catat Kematian](assets/readme/catatankematian.png)

## Riwayat Kematian

![Riwayat Kematian](assets/readme/riwayatkematian.png)

---

# 🎬 Project Preview

Video demonstrasi tersedia pada:

```text
assets/ceo.mp4
```

Video menunjukkan tampilan dan alur penggunaan sistem Sumber Aquarium PGK.

---

# 📚 Dokumentasi Akademik

Repository menyimpan artefak akademik:

```text
docs/Karil_Sumber_Aquarium_Kelompok_B.docx
docs/Sumber_Aquarium_PGK_Presentation.pptx
```

Dokumen tersebut digunakan sebagai bagian dari dokumentasi dan penyampaian hasil Capstone Project.

---

# 🧪 Status Project

```text
Project Type      : Academic Capstone Project
Scope             : Information System
Architecture      : Client / Server
Frontend           : HTML5 + CSS3 + Vanilla JavaScript
Backend            : Python + Flask
Database           : PostgreSQL
Database Adapter   : Psycopg 3
Authentication     : Session + Argon2
Rate Limiting      : Flask-Limiter
WSGI Server        : Gunicorn
Version Control    : Git
Repository         : GitHub
```

Project ini merupakan **prototype/sistem akademik**.

Implementasi saat ini ditujukan untuk demonstrasi kebutuhan dan proses sistem dalam konteks pembelajaran.

---

# ⚠️ Batasan Implementasi

Repository saat ini masih memiliki beberapa batasan yang perlu dipahami.

## 1. Belum terdapat automated test suite

Repository tidak memiliki direktori pengujian otomatis khusus untuk:

```text
API
Authentication
Transaction
Concurrency
Permission
Regression
```

Pengujian tersebut dapat menjadi pengembangan selanjutnya.

## 2. CSRF protection belum diimplementasikan

Autentikasi menggunakan session cookie, tetapi endpoint perubahan data belum menunjukkan mekanisme CSRF token khusus.

Perlindungan CSRF perlu dipertimbangkan sebelum deployment publik.

## 3. Rate limit menggunakan memory storage secara default

```text
memory://
```

Konfigurasi tersebut sesuai untuk penggunaan sederhana/development, tetapi shared storage lebih sesuai untuk deployment multi-worker.

## 4. Belum terdapat audit trail khusus

Histori penjualan dan kematian tersedia, tetapi belum terdapat audit trail generik yang mencatat seluruh aktivitas pengguna seperti:

```text
login
logout
create
update
delete
```

beserta identitas pengguna dan perubahan datanya.

## 5. Model pengguna masih sederhana

Sistem saat ini berpusat pada akun CEO dan belum menerapkan role-based access control yang lebih granular.

## 6. Belum terdapat integrasi sensor aquarium

Sistem belum menerima data sensor secara real-time seperti:

```text
temperature
pH
dissolved oxygen
ammonia
turbidity
```

Data tersebut berada di luar ruang lingkup implementasi repository saat ini.

---

# 🔭 Pengembangan Selanjutnya

Pengembangan dapat diarahkan pada beberapa area.

## Database

```text
Audit trail
Role-based access control
Supplier
Pembelian
Pelacakan pemasukan stok
Reporting
```

## Backend

```text
Automated testing
CSRF protection
API versioning
Structured logging
Observability
Shared rate-limit storage
```

## Frontend

```text
Pagination
Filtering lanjutan
Visual analytics
Improved validation
Accessibility improvements
```

## Operasional Aquarium

```text
Supplier management
Purchase records
Stock movement
Mortality analysis
Water-quality records
Sensor integration
```

---

# 🔎 Catatan tentang Data

Data yang tersedia pada:

```text
database/seed.sql
```

adalah **data contoh untuk kebutuhan project**.

Angka seperti:

```text
4.280 ekor
Rp162.660.000
```

merupakan hasil dari dataset seed repository.

Angka tersebut tidak boleh diperlakukan sebagai:

* data pasar;
* hasil survei harga;
* statistik industri;
* laporan keuangan bisnis aktual;
* hasil penelitian populasi ikan.

---

# 📖 Referensi Teknis

* Flask Documentation. Configuration and security documentation.
* PostgreSQL Documentation. Transactions and explicit locking.
* RFC 9106. *Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications*.
* Flask-Limiter Documentation.
* Gunicorn Documentation.
* Psycopg 3 Documentation.
* Universitas Terbuka. (2025). *Mengenal Capstone Project Mata Kuliah STSI4401*, Program Studi S1 Sistem Informasi, Fakultas Sains dan Teknologi.

---

# 📌 Ringkasan

Sumber Aquarium PGK mengintegrasikan:

```text
HTML5
   +
CSS3
   +
Vanilla JavaScript
   +
Python / Flask
   +
Psycopg 3
   +
PostgreSQL
   +
Argon2
   +
Flask-Limiter
   +
Gunicorn
```

dalam satu sistem informasi untuk:

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

Sistem ini dikembangkan sebagai **Capstone Project Kelompok B Program Studi S1 Sistem Informasi Universitas Terbuka** dan berfungsi sebagai implementasi akademik sistem informasi pengelolaan operasional toko ikan hias.

---

## Repository

Source code dan seluruh artefak project tersedia pada repository:

**Sumber Aquarium PGK — CAPSTONE_PROJECT_KELOMPOK_B**
