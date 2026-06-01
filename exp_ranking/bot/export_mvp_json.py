"""Export MVP JSON from SQLite without fetching new ranking data."""

from __future__ import annotations

import logging
import sys

import config
from analysis import build_analysis_rows
from mvp_export import export_mvp_json, filter_snapshots_for_history
from sqlite_storage import load_all_snapshots


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    config.load_env_file()

    snapshots = load_all_snapshots(config.sqlite_db_path())
    if not snapshots:
        logger.error("No snapshot rows in %s", config.sqlite_db_path())
        return 1

    min_level = config.ranking_min_level()
    latest_date = max(row.snapshot_date for row in snapshots)
    history_days = config.mvp_history_days()
    export_snapshots = filter_snapshots_for_history(
        snapshots,
        latest_date=latest_date,
        history_days=history_days,
    )
    export_top_n = config.mvp_export_top_n()

    analysis_rows = build_analysis_rows(
        snapshots,
        benchmark_character=config.benchmark_character_name(),
    )
    output_path = export_mvp_json(
        export_snapshots,
        analysis_rows,
        config.mvp_json_output_path(),
        export_top_n=export_top_n,
        ranking_min_level=min_level,
        latest_snapshot_date=latest_date,
        history_days=history_days,
    )
    logger.info("Exported MVP JSON to %s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
