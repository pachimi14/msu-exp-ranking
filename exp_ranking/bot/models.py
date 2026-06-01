"""Data models for snapshot and analysis sheets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SNAPSHOT_FIELDNAMES = [
    "snapshot_date",
    "rank",
    "rankFluctuation",
    "characterName",
    "classCode",
    "jobCode",
    "level",
    "exp",
    "imageUrl",
]

ANALYSIS_FIELDNAMES = [
    "snapshot_date",
    "rank",
    "characterName",
    "level",
    "exp",
    "total_exp_from_240",
    "daily_exp_gain",
    "exp_to_250",
    "diff_from_pachimi",
    "rankFluctuation",
]


@dataclass(frozen=True)
class SnapshotRow:
    snapshot_date: str
    rank: int
    rank_fluctuation: int
    character_name: str
    class_code: str
    job_code: str
    level: int
    exp: int
    image_url: str

    def as_row_values(self) -> list[Any]:
        return [
            self.snapshot_date,
            self.rank,
            self.rank_fluctuation,
            self.character_name,
            self.class_code,
            self.job_code,
            self.level,
            self.exp,
            self.image_url,
        ]


@dataclass(frozen=True)
class AnalysisRow:
    snapshot_date: str
    rank: int
    character_name: str
    level: int
    exp: int
    total_exp_from_240: int
    daily_exp_gain: int | None
    exp_to_250: int
    diff_from_pachimi: int | None
    rank_fluctuation: int

    def as_row_values(self) -> list[Any]:
        return [
            self.snapshot_date,
            self.rank,
            self.character_name,
            self.level,
            self.exp,
            self.total_exp_from_240,
            "" if self.daily_exp_gain is None else self.daily_exp_gain,
            self.exp_to_250,
            "" if self.diff_from_pachimi is None else self.diff_from_pachimi,
            self.rank_fluctuation,
        ]
