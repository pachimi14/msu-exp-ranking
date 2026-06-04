"""Tests for ranking-day skip logic."""

from __future__ import annotations

import os
from pathlib import Path
import tempfile
import shutil

from models import SnapshotRow
from ranking_day_skip import (
    ranking_day_already_captured,
    should_skip_ranking_fetch,
    try_skip_entire_run,
)
from sqlite_storage import append_snapshots, init_db


def test_skip_when_enough_rows() -> None:
    tmpdir = Path(tempfile.mkdtemp())
    db = tmpdir / "t.db"
    try:
        init_db(db)
        rows = [
            SnapshotRow(
                "2026-06-05", i, 0, f"C{i}", "", "", 248, 1, "", f"k{i}"
            )
            for i in range(1, 1100)
        ]
        append_snapshots(db, rows, "2026-06-05T00:00:00")
        assert ranking_day_already_captured(db, "2026-06-05")
        old_skip = os.environ.get("SKIP_RUN_IF_RANKING_DAY_EXISTS")
        old_deploy = os.environ.get("SKIP_DEPLOY_IF_DAY_CAPTURED")
        os.environ["SKIP_RUN_IF_RANKING_DAY_EXISTS"] = "true"
        os.environ["SKIP_DEPLOY_IF_DAY_CAPTURED"] = "true"
        try:
            assert should_skip_ranking_fetch(db, "2026-06-05")
            assert try_skip_entire_run(db, "2026-06-05")
            os.environ["SKIP_DEPLOY_IF_DAY_CAPTURED"] = "false"
            assert should_skip_ranking_fetch(db, "2026-06-05")
            assert not try_skip_entire_run(db, "2026-06-05")
        finally:
            for key, value in (
                ("SKIP_RUN_IF_RANKING_DAY_EXISTS", old_skip),
                ("SKIP_DEPLOY_IF_DAY_CAPTURED", old_deploy),
            ):
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    test_skip_when_enough_rows()
    print("ok")
