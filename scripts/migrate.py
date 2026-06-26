#!/usr/bin/env python3
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def ensure_database(host: str, port: str, db: str, root_db: str, root_user: str, root_password: str) -> None:
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=root_db,
        user=root_user,
        password=root_password,
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db,))
            if cur.fetchone() is None:
                cur.execute(f"CREATE DATABASE {qident(db)}")
    finally:
        conn.close()


def main() -> None:
    load_dotenv()
    root = Path(__file__).resolve().parents[1]
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    root_db = os.getenv("POSTGRES_ROOT_DB", "root_db")
    root_user = os.getenv("POSTGRES_ROOT_USER", "ouros_root")
    root_password = os.getenv("POSTGRES_ROOT_PASSWORD", "root")
    ensure_database(host, port, db, root_db, root_user, root_password)
    print(f"PostgreSQL migrations scaffold at {root} using {host}:{port}/{db}")


if __name__ == "__main__":
    main()
