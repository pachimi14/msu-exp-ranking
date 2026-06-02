"""SQLite storage for ranking snapshots."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from models import SnapshotRow

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS ranking_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL,
    rank INTEGER NOT NULL,
    rank_fluctuation INTEGER NOT NULL DEFAULT 0,
    character_name TEXT NOT NULL,
    class_code TEXT NOT NULL DEFAULT '',
    job_code TEXT NOT NULL DEFAULT '',
    level INTEGER NOT NULL,
    exp INTEGER NOT NULL,
    image_url TEXT NOT NULL DEFAULT '',
    character_asset_key TEXT NOT NULL DEFAULT '',
    fetched_at TEXT NOT NULL,
    UNIQUE(snapshot_date, rank)
);

CREATE INDEX IF NOT EXISTS idx_ranking_snapshot_date
    ON ranking_snapshot(snapshot_date);

CREATE INDEX IF NOT EXISTS idx_ranking_snapshot_character
    ON ranking_snapshot(character_name);

CREATE TABLE IF NOT EXISTS character_meta (
    character_asset_key TEXT PRIMARY KEY,
    world_id TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
"""


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {str(row[1]) for row in rows}


def _migrate_schema(conn: sqlite3.Connection) -> None:
    snapshot_columns = _table_columns(conn, "ranking_snapshot")
    if "character_asset_key" not in snapshot_columns:
        conn.execute(
            """
            ALTER TABLE ranking_snapshot
            ADD COLUMN character_asset_key TEXT NOT NULL DEFAULT ''
            """
        )


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(_SCHEMA)
        _migrate_schema(conn)
        conn.commit()


def append_snapshots(
    db_path: Path,
    rows: list[SnapshotRow],
    fetched_at: str,
) -> tuple[int, int]:
    init_db(db_path)
    saved = 0
    skipped = 0

    with sqlite3.connect(db_path) as conn:
        for row in rows:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO ranking_snapshot (
                    snapshot_date, rank, rank_fluctuation, character_name,
                    class_code, job_code, level, exp, image_url,
                    character_asset_key, fetched_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.snapshot_date,
                    row.rank,
                    row.rank_fluctuation,
                    row.character_name,
                    row.class_code,
                    row.job_code,
                    row.level,
                    row.exp,
                    row.image_url,
                    row.character_asset_key,
                    fetched_at,
                ),
            )
            if cursor.rowcount > 0:
                saved += 1
            else:
                skipped += 1
        conn.commit()

    logger.info(
        "SQLite snapshot: saved=%s skipped=%s db=%s",
        saved,
        skipped,
        db_path,
    )
    return saved, skipped


def load_all_snapshots(db_path: Path) -> list[SnapshotRow]:
    if not db_path.exists():
        return []

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT
                snapshot_date, rank, rank_fluctuation, character_name,
                class_code, job_code, level, exp, image_url, character_asset_key
            FROM ranking_snapshot
            ORDER BY snapshot_date ASC, rank ASC
            """
        ).fetchall()

    return [
        SnapshotRow(
            snapshot_date=str(row["snapshot_date"]),
            rank=int(row["rank"]),
            rank_fluctuation=int(row["rank_fluctuation"]),
            character_name=str(row["character_name"]),
            class_code=str(row["class_code"]),
            job_code=str(row["job_code"]),
            level=int(row["level"]),
            exp=int(row["exp"]),
            image_url=str(row["image_url"]),
            character_asset_key=str(row["character_asset_key"] or ""),
        )
        for row in rows
    ]


def load_character_meta(db_path: Path) -> dict[str, str]:
    if not db_path.exists():
        return {}

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT character_asset_key, world_id
            FROM character_meta
            WHERE character_asset_key != ''
            """
        ).fetchall()

    return {str(row[0]): str(row[1] or "") for row in rows}


def upsert_character_meta(
    db_path: Path,
    character_asset_key: str,
    world_id: str,
    updated_at: str,
) -> None:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO character_meta (character_asset_key, world_id, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(character_asset_key) DO UPDATE SET
                world_id = excluded.world_id,
                updated_at = excluded.updated_at
            """,
            (character_asset_key, world_id, updated_at),
        )
        conn.commit()


def count_snapshots(db_path: Path) -> int:
    if not db_path.exists():
        return 0
    with sqlite3.connect(db_path) as conn:
        result = conn.execute("SELECT COUNT(*) FROM ranking_snapshot").fetchone()
    return int(result[0]) if result else 0


def delete_snapshots_before(db_path: Path, cutoff_date: str) -> int:
    """Delete rows with snapshot_date strictly before cutoff_date."""
    if not db_path.exists():
        return 0

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM ranking_snapshot WHERE snapshot_date < ?",
            (cutoff_date,),
        )
        deleted = cursor.rowcount
        conn.commit()

    logger.info(
        "Deleted snapshots before %s: rows=%s db=%s",
        cutoff_date,
        deleted,
        db_path,
    )
    return deleted


def latest_snapshot_date(db_path: Path) -> str | None:
    if not db_path.exists():
        return None
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT MAX(snapshot_date) FROM ranking_snapshot"
        ).fetchone()
    return str(row[0]) if row and row[0] else None
