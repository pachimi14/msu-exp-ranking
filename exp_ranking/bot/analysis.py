"""Build ranking_analysis rows from snapshot data."""

from __future__ import annotations

from models import AnalysisRow, SnapshotRow
from level_exp import (
    calculate_exp_to_250,
    calculate_progress_toward_250,
    calculate_total_exp_from_240,
)
from utils import normalize_int


def build_analysis_rows(
    snapshots: list[SnapshotRow],
    benchmark_character: str = "pachimi",
) -> list[AnalysisRow]:
    if not snapshots:
        return []

    ordered = sorted(
        snapshots,
        key=lambda row: (row.snapshot_date, row.rank),
    )

    totals_by_character: dict[str, list[tuple[str, int]]] = {}
    totals_by_date: dict[str, dict[str, int]] = {}

    analysis_rows: list[AnalysisRow] = []

    for row in ordered:
        total_exp = calculate_total_exp_from_240(row.level, row.exp)
        progress = calculate_progress_toward_250(row.level, row.exp)
        character_key = row.character_name.casefold()

        history = totals_by_character.setdefault(character_key, [])
        daily_gain: int | None = None
        if history:
            daily_gain = progress - history[-1][1]
        history.append((row.snapshot_date, progress))

        date_totals = totals_by_date.setdefault(row.snapshot_date, {})
        date_totals[character_key] = total_exp

        analysis_rows.append(
            AnalysisRow(
                snapshot_date=row.snapshot_date,
                rank=row.rank,
                character_name=row.character_name,
                level=row.level,
                exp=row.exp,
                total_exp_from_240=total_exp,
                daily_exp_gain=daily_gain,
                exp_to_250=calculate_exp_to_250(row.level, row.exp),
                diff_from_pachimi=None,
                rank_fluctuation=row.rank_fluctuation,
            )
        )

    benchmark_key = benchmark_character.casefold()
    for index, row in enumerate(analysis_rows):
        pachimi_total = totals_by_date.get(row.snapshot_date, {}).get(benchmark_key)
        if pachimi_total is None:
            continue
        current = analysis_rows[index]
        analysis_rows[index] = AnalysisRow(
            snapshot_date=current.snapshot_date,
            rank=current.rank,
            character_name=current.character_name,
            level=current.level,
            exp=current.exp,
            total_exp_from_240=current.total_exp_from_240,
            daily_exp_gain=current.daily_exp_gain,
            exp_to_250=current.exp_to_250,
            diff_from_pachimi=current.total_exp_from_240 - pachimi_total,
            rank_fluctuation=current.rank_fluctuation,
        )

    return analysis_rows


def snapshot_from_record(record: dict[str, object]) -> SnapshotRow:
    return SnapshotRow(
        snapshot_date=str(record.get("snapshot_date", "")).strip(),
        rank=normalize_int(record.get("rank")),
        rank_fluctuation=normalize_int(record.get("rankFluctuation")),
        character_name=str(record.get("characterName", "")).strip(),
        class_code=str(record.get("classCode", "")).strip(),
        job_code=str(record.get("jobCode", "")).strip(),
        level=normalize_int(record.get("level")),
        exp=normalize_int(record.get("exp")),
        image_url=str(record.get("imageUrl", "")).strip(),
    )
