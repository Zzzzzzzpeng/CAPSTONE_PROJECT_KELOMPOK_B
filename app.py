from __future__ import annotations

import logging
import os
import secrets
from decimal import Decimal, InvalidOperation
from functools import wraps
from pathlib import Path

import psycopg
from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, send_from_directory, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from psycopg.errors import ForeignKeyViolation

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DASHBOARD_PATH = os.getenv("DASHBOARD_PATH", "/dashboard.html")
DEFAULT_FISH_PHOTO = "/assets/images/logo.png"

app = Flask(__name__, static_folder=None)

app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE=os.getenv(
        "SESSION_COOKIE_SAMESITE",
        "Lax",
    ),
    SESSION_COOKIE_SECURE=os.getenv(
        "SESSION_COOKIE_SECURE",
        "0",
    ).lower() in {"1", "true", "yes"},
    MAX_CONTENT_LENGTH=64 * 1024,
)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper()
)

log = logging.getLogger("sumber-aquarium")

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["300 per minute"],
    storage_uri=os.getenv(
        "RATELIMIT_STORAGE_URI",
        "memory://",
    ),
)

ph = PasswordHasher()


# ============================================================
# SECURITY HEADERS
# ============================================================

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"

    return response


# ============================================================
# DATABASE
# ============================================================

def get_db():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url)

    required = (
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    )

    missing = [
        name
        for name in required
        if not os.getenv(name)
    ]

    if missing:
        raise RuntimeError(
            "Missing database environment variables: "
            + ", ".join(missing)
        )

    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


# ============================================================
# HELPERS
# ============================================================

def api_error(message: str, status: int):
    return jsonify({"error": message}), status


def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("ceo_id"):
            return api_error(
                "Authentication required.",
                401,
            )

        return view(*args, **kwargs)

    return wrapper


def text_value(value, field: str, limit: int):
    if value is None or not str(value).strip():
        raise ValueError(
            f"Field '{field}' wajib diisi."
        )

    value = str(value).strip()

    if len(value) > limit:
        raise ValueError(
            f"Field '{field}' terlalu panjang."
        )

    return value


def integer_value(
    value,
    field: str,
    minimum: int = 0,
):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"Field '{field}' harus berupa angka bulat."
        )

    if value < minimum:
        raise ValueError(
            f"Field '{field}' minimal {minimum}."
        )

    return value


def money_value(value):
    try:
        value = Decimal(str(value))
    except (
        InvalidOperation,
        TypeError,
        ValueError,
    ):
        raise ValueError(
            "Field 'harga' harus berupa angka."
        )

    if value < 0:
        raise ValueError(
            "Harga tidak boleh negatif."
        )

    if value.as_tuple().exponent < -2:
        raise ValueError(
            "Harga maksimal memiliki 2 angka desimal."
        )

    return value


def fish_json(row):
    return {
        "id": row[0],
        "nama": row[1],
        "foto": row[2],
        "kategori": row[3],
        "jumlah": row[4],
        "harga": float(row[5]),
    }


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(413)
def payload_too_large(_error):
    return api_error(
        "Request terlalu besar.",
        413,
    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")

        return jsonify({
            "status": "ok",
            "database": os.getenv(
                "DB_NAME",
                "configured",
            ),
        })

    except Exception:
        log.exception("Health check failed")

        return jsonify({
            "status": "error",
            "database": "unavailable",
        }), 503


# ============================================================
# FISH
# ============================================================

@app.get("/api/ikan")
@auth_required
def list_fish():
    try:
        with get_db() as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga
                FROM ikan
                ORDER BY id
                """
            ).fetchall()

        return jsonify([
            fish_json(row)
            for row in rows
        ])

    except Exception:
        log.exception("List fish failed")

        return api_error(
            "Gagal mengambil data ikan.",
            500,
        )


@app.get("/api/ikan/<int:fish_id>")
@auth_required
def get_fish(fish_id):
    try:
        with get_db() as conn:
            row = conn.execute(
                """
                SELECT
                    id,
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga
                FROM ikan
                WHERE id = %s
                """,
                (fish_id,),
            ).fetchone()

        if row is None:
            return api_error(
                "Data ikan tidak ditemukan.",
                404,
            )

        return jsonify(fish_json(row))

    except Exception:
        log.exception("Get fish failed")

        return api_error(
            "Gagal mengambil data ikan.",
            500,
        )


@app.post("/api/ikan")
@auth_required
def add_fish():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return api_error(
            "Body JSON tidak valid.",
            400,
        )

    try:
        nama = text_value(
            data.get("nama"),
            "nama",
            100,
        )

        foto = str(
            data.get("foto")
            or DEFAULT_FISH_PHOTO
        ).strip()

        if len(foto) > 500:
            raise ValueError(
                "Field 'foto' terlalu panjang."
            )

        kategori = text_value(
            data.get("kategori"),
            "kategori",
            100,
        )

        jumlah = integer_value(
            data.get("jumlah"),
            "jumlah",
        )

        harga = money_value(
            data.get("harga")
        )

        with get_db() as conn:
            row = conn.execute(
                """
                INSERT INTO ikan (
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING
                    id,
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga
                """,
                (
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga,
                ),
            ).fetchone()

            conn.commit()

        return jsonify(
            fish_json(row)
        ), 201

    except ValueError as exc:
        return api_error(
            str(exc),
            400,
        )

    except Exception:
        log.exception("Add fish failed")

        return api_error(
            "Gagal menyimpan data ikan.",
            500,
        )


@app.put("/api/ikan/<int:fish_id>")
@auth_required
def edit_fish(fish_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return api_error(
            "Body JSON tidak valid.",
            400,
        )

    try:
        nama = text_value(
            data.get("nama"),
            "nama",
            100,
        )

        foto = str(
            data.get("foto")
            or DEFAULT_FISH_PHOTO
        ).strip()

        if len(foto) > 500:
            raise ValueError(
                "Field 'foto' terlalu panjang."
            )

        kategori = text_value(
            data.get("kategori"),
            "kategori",
            100,
        )

        jumlah = integer_value(
            data.get("jumlah"),
            "jumlah",
        )

        harga = money_value(
            data.get("harga")
        )

        with get_db() as conn:
            row = conn.execute(
                """
                UPDATE ikan
                SET
                    nama = %s,
                    foto = %s,
                    kategori = %s,
                    jumlah = %s,
                    harga = %s
                WHERE id = %s
                RETURNING
                    id,
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga
                """,
                (
                    nama,
                    foto,
                    kategori,
                    jumlah,
                    harga,
                    fish_id,
                ),
            ).fetchone()

            if row is None:
                return api_error(
                    "Data ikan tidak ditemukan.",
                    404,
                )

            conn.commit()

        return jsonify(
            fish_json(row)
        )

    except ValueError as exc:
        return api_error(
            str(exc),
            400,
        )

    except Exception:
        log.exception("Edit fish failed")

        return api_error(
            "Gagal memperbarui data ikan.",
            500,
        )


# ============================================================
# BULK SYNC
# ============================================================

@app.put("/api/ikan")
@auth_required
def sync_fish():
    data = request.get_json(silent=True)

    if not isinstance(data, list):
        return api_error(
            "Payload harus berupa array.",
            400,
        )

    try:
        rows = []
        seen_ids = set()

        for item in data:
            if not isinstance(item, dict):
                raise ValueError(
                    "Item sync tidak valid."
                )

            fish_id = integer_value(
                item.get("id"),
                "id",
                1,
            )

            if fish_id in seen_ids:
                raise ValueError(
                    "ID ikan duplikat."
                )

            seen_ids.add(fish_id)

            foto = str(
                item.get("foto")
                or DEFAULT_FISH_PHOTO
            ).strip()

            if len(foto) > 500:
                raise ValueError(
                    "Field 'foto' terlalu panjang."
                )

            rows.append((
                fish_id,
                text_value(
                    item.get("nama"),
                    "nama",
                    100,
                ),
                foto,
                text_value(
                    item.get("kategori"),
                    "kategori",
                    100,
                ),
                integer_value(
                    item.get("jumlah"),
                    "jumlah",
                ),
                money_value(
                    item.get("harga")
                ),
            ))

        with get_db() as conn:
            with conn.transaction():
                for row in rows:
                    conn.execute(
                        """
                        INSERT INTO ikan (
                            id,
                            nama,
                            foto,
                            kategori,
                            jumlah,
                            harga
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (id)
                        DO UPDATE SET
                            nama = EXCLUDED.nama,
                            foto = EXCLUDED.foto,
                            kategori = EXCLUDED.kategori,
                            jumlah = EXCLUDED.jumlah,
                            harga = EXCLUDED.harga
                        """,
                        row,
                    )

                if rows:
                    conn.execute(
                        """
                        SELECT setval(
                            pg_get_serial_sequence(
                                'ikan',
                                'id'
                            ),
                            GREATEST(
                                COALESCE(
                                    (
                                        SELECT MAX(id)
                                        FROM ikan
                                    ),
                                    1
                                ),
                                1
                            ),
                            true
                        )
                        """
                    )

        return jsonify({
            "message": (
                "Data ikan berhasil disinkronkan."
            ),
            "count": len(rows),
        })

    except ValueError as exc:
        return api_error(
            str(exc),
            400,
        )

    except Exception:
        log.exception("Sync fish failed")

        return api_error(
            "Gagal menyinkronkan data ikan.",
            500,
        )


# ============================================================
# DELETE FISH
# ============================================================

@app.delete("/api/ikan/<int:fish_id>")
@auth_required
def remove_fish(fish_id):
    try:
        with get_db() as conn:
            result = conn.execute(
                """
                DELETE FROM ikan
                WHERE id = %s
                """,
                (fish_id,),
            )

            if result.rowcount == 0:
                return api_error(
                    "Data ikan tidak ditemukan.",
                    404,
                )

            conn.commit()

        return jsonify({
            "message": (
                "Data ikan berhasil dihapus."
            ),
        })

    except ForeignKeyViolation:
        return api_error(
            (
                "Ikan tidak dapat dihapus karena "
                "sudah memiliki riwayat penjualan "
                "atau kematian."
            ),
            409,
        )

    except Exception:
        log.exception(
            "Delete fish failed"
        )

        return api_error(
            "Gagal menghapus data ikan.",
            500,
        )


# ============================================================
# DEATH HISTORY
# ============================================================

@app.get("/api/kematian")
@auth_required
def death_history():
    try:
        with get_db() as conn:
            rows = conn.execute(
                """
                SELECT
                    rk.id,
                    rk.ikan_id,
                    i.nama,
                    rk.jumlah,
                    rk.keterangan,
                    rk.created_at
                FROM riwayat_kematian rk
                JOIN ikan i
                    ON i.id = rk.ikan_id
                ORDER BY
                    rk.created_at DESC,
                    rk.id DESC
                """
            ).fetchall()

        return jsonify([
            {
                "id": row[0],
                "ikan_id": row[1],
                "namaIkan": row[2],
                "jumlah": row[3],
                "keterangan": row[4],
                "tanggal": row[5].isoformat(),
            }
            for row in rows
        ])

    except Exception:
        log.exception(
            "Death history failed"
        )

        return api_error(
            "Gagal mengambil riwayat kematian.",
            500,
        )


# ============================================================
# CREATE DEATH
# ============================================================

@app.post("/api/kematian")
@auth_required
def add_death():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return api_error(
            "Body JSON tidak valid.",
            400,
        )

    try:
        fish_id = integer_value(
            data.get("ikan_id"),
            "ikan_id",
            1,
        )

        amount = integer_value(
            data.get("jumlah"),
            "jumlah",
            1,
        )

        note = text_value(
            data.get("keterangan"),
            "keterangan",
            1000,
        )

        with get_db() as conn:
            with conn.transaction():
                fish = conn.execute(
                    """
                    SELECT
                        id,
                        nama,
                        jumlah
                    FROM ikan
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (fish_id,),
                ).fetchone()

                if fish is None:
                    return api_error(
                        "Data ikan tidak ditemukan.",
                        404,
                    )

                if fish[2] < amount:
                    return api_error(
                        (
                            f"Stok {fish[1]} hanya "
                            f"{fish[2]} ekor."
                        ),
                        400,
                    )

                updated = conn.execute(
                    """
                    UPDATE ikan
                    SET jumlah = jumlah - %s
                    WHERE id = %s
                    RETURNING
                        id,
                        nama,
                        jumlah
                    """,
                    (
                        amount,
                        fish_id,
                    ),
                ).fetchone()

                history = conn.execute(
                    """
                    INSERT INTO riwayat_kematian (
                        ikan_id,
                        jumlah,
                        keterangan
                    )
                    VALUES (%s, %s, %s)
                    RETURNING
                        id,
                        created_at
                    """,
                    (
                        fish_id,
                        amount,
                        note,
                    ),
                ).fetchone()

        return jsonify({
            "message": (
                "Data kematian berhasil dicatat."
            ),
            "data": {
                "id": history[0],
                "ikan_id": updated[0],
                "namaIkan": updated[1],
                "jumlahMati": amount,
                "stokSekarang": updated[2],
                "keterangan": note,
                "created_at": (
                    history[1].isoformat()
                ),
            },
        }), 201

    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        return api_error(
            str(exc)
            or "Data request tidak valid.",
            400,
        )

    except Exception:
        log.exception(
            "Add death failed"
        )

        return api_error(
            "Gagal mencatat kematian.",
            500,
        )


# ============================================================
# SALES HISTORY
# ============================================================

@app.get("/api/penjualan")
@auth_required
def sales_history():
    try:
        with get_db() as conn:
            rows = conn.execute(
                """
                SELECT
                    rp.id,
                    rp.ikan_id,
                    i.nama,
                    rp.jumlah,
                    rp.harga_satuan,
                    rp.total_harga,
                    rp.created_at
                FROM riwayat_penjualan rp
                JOIN ikan i
                    ON i.id = rp.ikan_id
                ORDER BY
                    rp.created_at DESC,
                    rp.id DESC
                """
            ).fetchall()

        return jsonify([
            {
                "id": row[0],
                "ikan_id": row[1],
                "namaIkan": row[2],
                "jumlah": row[3],
                "hargaSatuan": float(row[4]),
                "totalHarga": float(row[5]),
                "tanggal": row[6].isoformat(),
            }
            for row in rows
        ])

    except Exception:
        log.exception(
            "Sales history failed"
        )

        return api_error(
            "Gagal mengambil riwayat penjualan.",
            500,
        )


# ============================================================
# CREATE SALE
# ============================================================

@app.post("/api/penjualan")
@auth_required
def add_sale():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return api_error(
            "Body JSON tidak valid.",
            400,
        )

    try:
        fish_id = integer_value(
            data.get("ikan_id"),
            "ikan_id",
            1,
        )

        amount = integer_value(
            data.get("jumlah"),
            "jumlah",
            1,
        )

        with get_db() as conn:
            with conn.transaction():
                fish = conn.execute(
                    """
                    SELECT
                        id,
                        nama,
                        jumlah,
                        harga
                    FROM ikan
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (fish_id,),
                ).fetchone()

                if fish is None:
                    return api_error(
                        "Data ikan tidak ditemukan.",
                        404,
                    )

                if fish[2] < amount:
                    return api_error(
                        (
                            f"Stok {fish[1]} hanya "
                            f"{fish[2]} ekor."
                        ),
                        400,
                    )

                total = fish[3] * amount

                updated = conn.execute(
                    """
                    UPDATE ikan
                    SET jumlah = jumlah - %s
                    WHERE id = %s
                    RETURNING
                        id,
                        nama,
                        jumlah
                    """,
                    (
                        amount,
                        fish_id,
                    ),
                ).fetchone()

                sale = conn.execute(
                    """
                    INSERT INTO riwayat_penjualan (
                        ikan_id,
                        jumlah,
                        harga_satuan,
                        total_harga
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING
                        id,
                        created_at
                    """,
                    (
                        fish_id,
                        amount,
                        fish[3],
                        total,
                    ),
                ).fetchone()

        return jsonify({
            "message": (
                "Transaksi penjualan berhasil disimpan."
            ),
            "data": {
                "id": sale[0],
                "ikan_id": updated[0],
                "namaIkan": updated[1],
                "jumlah": amount,
                "hargaSatuan": float(
                    fish[3]
                ),
                "totalHarga": float(
                    total
                ),
                "stokSekarang": updated[2],
                "created_at": (
                    sale[1].isoformat()
                ),
            },
        }), 201

    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        return api_error(
            str(exc)
            or "Data request tidak valid.",
            400,
        )

    except Exception:
        log.exception(
            "Add sale failed"
        )

        return api_error(
            "Gagal menyimpan transaksi penjualan.",
            500,
        )


# ============================================================
# AUTH LOGIN
# ============================================================

@app.post("/api/auth/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json(
        silent=True
    ) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = str(
        data.get("password", "")
    )

    if not username or not password:
        return jsonify({
            "message": (
                "Username dan password wajib diisi."
            ),
        }), 400

    if (
        len(username) > 64
        or len(password) > 128
    ):
        return jsonify({
            "message": "Credential tidak valid.",
        }), 400

    try:
        with get_db() as conn:
            row = conn.execute(
                """
                SELECT
                    id,
                    username,
                    password_hash
                FROM ceo_accounts
                WHERE username = %s
                  AND is_active = TRUE
                """,
                (username,),
            ).fetchone()

        if row is None:
            return jsonify({
                "message": (
                    "Username atau password salah."
                ),
            }), 401

        try:
            ph.verify(
                row[2],
                password,
            )

        except (
            VerifyMismatchError,
            VerificationError,
            InvalidHashError,
        ):
            return jsonify({
                "message": (
                    "Username atau password salah."
                ),
            }), 401

        session.clear()

        session["ceo_id"] = row[0]
        session["ceo_username"] = row[1]

        return jsonify({
            "message": (
                "CEO authentication successful."
            ),
            "username": row[1],
            "redirect": DASHBOARD_PATH,
        })

    except Exception:
        log.exception(
            "Login failed"
        )

        return jsonify({
            "message": (
                "Layanan autentikasi sedang bermasalah."
            ),
        }), 500


@app.get("/api/auth/me")
def auth_me():
    if not session.get("ceo_id"):
        return jsonify({
            "authenticated": False,
        }), 401

    return jsonify({
        "authenticated": True,
        "id": session["ceo_id"],
        "username": session.get(
            "ceo_username"
        ),
    })


@app.post("/api/auth/logout")
def logout():
    session.clear()

    return jsonify({
        "message": "Logged out.",
    })


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
@app.get("/login")
@app.get("/login.html")
def login_page():
    if session.get("ceo_id"):
        return redirect(
            DASHBOARD_PATH
        )

    response = send_from_directory(
        BASE_DIR / "login",
        "login.html",
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"

    return response


@app.get("/dashboard.html")
@app.get("/dasboard.html")
@auth_required
def dashboard():
    return send_from_directory(
        BASE_DIR,
        "dashboard.html",
    )


@app.get("/CEO.html")
@auth_required
def ceo():
    return send_from_directory(
        BASE_DIR,
        "CEO.html",
    )


@app.get("/<path:path>")
def frontend(path):
    path = path.lstrip("/")

    protected = (
        path in {
            "dashboard.html",
            "dasboard.html",
            "CEO.html",
        }
        or path.startswith("modules/")
    )

    if protected and not session.get("ceo_id"):
        return redirect("/")

    candidate = (
        BASE_DIR / path
    ).resolve()

    try:
        candidate.relative_to(
            BASE_DIR
        )
    except ValueError:
        return api_error(
            "File tidak ditemukan.",
            404,
        )

    if not candidate.is_file():
        return api_error(
            "File tidak ditemukan.",
            404,
        )

    response = send_from_directory(
        BASE_DIR,
        path,
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    return response


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(
        host=os.getenv(
            "HOST",
            "127.0.0.1",
        ),
        port=int(
            os.getenv(
                "PORT",
                "5000",
            )
        ),
        debug=os.getenv(
            "FLASK_DEBUG",
            "0",
        ).lower() in {
            "1",
            "true",
            "yes",
        },
    )
