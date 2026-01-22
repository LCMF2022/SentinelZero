import sqlite3
import time
from typing import Optional

DB_PATH = "sentinelzero_cache.db"
TTL_SECONDS = 24 * 60 * 60  # 24h


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at INTEGER
        )
        """)


def get_cache(key: str) -> Optional[str]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT value, updated_at FROM cache WHERE key = ?",
            (key,)
        )
        row = cur.fetchone()
        if not row:
            return None

        value, ts = row
        if time.time() - ts > TTL_SECONDS:
            return None

        return value


def set_cache(key: str, value: str):
    with get_connection() as conn:
        conn.execute(
            "REPLACE INTO cache (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, int(time.time()))
        )
