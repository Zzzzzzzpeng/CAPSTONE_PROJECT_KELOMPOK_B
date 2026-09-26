
import argparse
import os
import sys
from getpass import getpass

import psycopg
from argon2 import PasswordHasher
from dotenv import load_dotenv

load_dotenv()
ph = PasswordHasher()


def get_args():
    parser = argparse.ArgumentParser(description="Create a CEO account securely.")
    parser.add_argument("--username", default=None, help="CEO username")
    return parser.parse_args()


def main():
    args = get_args()
    username = (args.username or input("CEO username: ")).strip()

    if not username:
        print("ERROR: username cannot be empty.")
        return 1

    password = getpass("CEO password: ")
    confirm = getpass("Repeat password: ")

    if not password:
        print("ERROR: password cannot be empty.")
        return 1
    if password != confirm:
        print("ERROR: passwords do not match.")
        return 1

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        name = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password_db = os.getenv("DB_PASSWORD")

        required = {
            "DB_HOST": host,
            "DB_PORT": port,
            "DB_NAME": name,
            "DB_USER": user,
            "DB_PASSWORD": password_db,
        }
        missing = [key for key, value in required.items() if value is None]
        if missing:
            print(
                "ERROR: missing database environment variables: "
                + ", ".join(missing),
                file=sys.stderr,
            )
            return 1

        db_url = (
            f"host={host} port={port} dbname={name} "
            f"user={user} password={password_db}"
        )

    password_hash = ph.hash(password)

    # Expected table:
    #   ceo_accounts(id, username, password_hash, is_active)
    # Adjust the table/column names here if your schema uses different names.
    sql = """
        INSERT INTO ceo_accounts (username, password_hash, is_active)
        VALUES (%s, %s, TRUE)
        ON CONFLICT (username)
        DO UPDATE SET password_hash = EXCLUDED.password_hash,
                      is_active = TRUE
    """

    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, password_hash))
        print(f"CEO account ready: {username}")
        print("Password stored as an Argon2 hash, not plaintext.")
        return 0
    except psycopg.Error as exc:
        print(f"DATABASE ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
