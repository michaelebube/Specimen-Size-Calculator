from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Tuple

import psycopg
from psycopg.rows import dict_row

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "specimens.db"


def _get_database_url() -> str:
    """Return normalized database URL from env, if configured."""
    raw_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_url:
        return ""

    if raw_url.startswith("postgres://"):
        return "postgresql://" + raw_url[len("postgres://") :]

    return raw_url


def _use_postgres() -> bool:
    return bool(_get_database_url())


def ensure_database() -> None:
    """Create the database and table if they do not already exist."""
    if _use_postgres():
        with psycopg.connect(_get_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS specimen_records (
                        id BIGSERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        microscope_size DOUBLE PRECISION NOT NULL,
                        magnification DOUBLE PRECISION NOT NULL,
                        actual_size DOUBLE PRECISION NOT NULL,
                        unit TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
            conn.commit()
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS specimen_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                microscope_size REAL NOT NULL,
                magnification REAL NOT NULL,
                actual_size REAL NOT NULL,
                unit TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def calculate_actual_size(microscope_size: float, magnification: float) -> float:
    """Actual size formula: actual size = microscope size / magnification."""
    if microscope_size <= 0:
        raise ValueError("Microscope size must be greater than 0.")
    if magnification <= 0:
        raise ValueError("Magnification must be greater than 0.")

    return microscope_size / magnification


def store_record(
    username: str,
    microscope_size: float,
    magnification: float,
    unit: str = "um",
) -> Tuple[int, float]:
    """Calculate actual size and persist a record to SQLite."""
    clean_username = username.strip()
    clean_unit = unit.strip() or "um"

    if not clean_username:
        raise ValueError("Username is required.")

    actual_size = calculate_actual_size(microscope_size, magnification)
    ensure_database()

    if _use_postgres():
        with psycopg.connect(_get_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO specimen_records (username, microscope_size, magnification, actual_size, unit)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        clean_username,
                        microscope_size,
                        magnification,
                        actual_size,
                        clean_unit,
                    ),
                )
                row = cur.fetchone()
            conn.commit()

        record_id = int(row[0]) if row else 0
        return record_id, actual_size

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO specimen_records (username, microscope_size, magnification, actual_size, unit)
            VALUES (?, ?, ?, ?, ?)
            """,
            (clean_username, microscope_size, magnification, actual_size, clean_unit),
        )
        conn.commit()
        record_id = int(cursor.lastrowid)

    return record_id, actual_size


def fetch_records(limit: int = 100) -> List[Dict[str, Any]]:
    """Return latest stored records for display in GUI/web UI."""
    ensure_database()

    if _use_postgres():
        with psycopg.connect(_get_database_url(), row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, username, microscope_size, magnification, actual_size, unit, created_at
                    FROM specimen_records
                    ORDER BY id DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                rows = cur.fetchall()

        for row in rows:
            created_at = row.get("created_at")
            if created_at is not None:
                row["created_at"] = str(created_at)
        return rows

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, username, microscope_size, magnification, actual_size, unit, created_at
            FROM specimen_records
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
