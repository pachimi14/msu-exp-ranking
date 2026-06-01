"""Shared helpers."""

from __future__ import annotations

from typing import Any


def normalize_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    text = str(value).strip().replace(",", "")
    if not text:
        return default
    return int(float(text))
