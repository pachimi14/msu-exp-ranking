"""Stable character identity across ranking days (asset key + name fallback)."""

from __future__ import annotations

from typing import Any

from models import SnapshotRow


def build_name_to_asset_key(snapshots: list[SnapshotRow]) -> dict[str, str]:
    """Map character name -> asset key using snapshot rows (prefer latest day)."""
    if not snapshots:
        return {}

    latest_date = max(row.snapshot_date for row in snapshots)
    latest_rows = [row for row in snapshots if row.snapshot_date == latest_date]
    return _name_to_asset_key_from_snapshot_rows(latest_rows)


def _name_to_asset_key_from_snapshot_rows(rows: list[SnapshotRow]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in rows:
        asset_key = (row.character_asset_key or "").strip()
        name = (row.character_name or "").strip()
        if asset_key and name:
            mapping[name.casefold()] = asset_key
    return mapping


def build_name_to_asset_key_from_ranking(ranking: list[dict[str, Any]]) -> dict[str, str]:
    """Map character name -> asset key from today's ranking API payload."""
    from navigator import extract_asset_key

    mapping: dict[str, str] = {}
    for entry in ranking:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("characterName") or "").strip()
        asset_key = extract_asset_key(entry)
        if name and asset_key:
            mapping[name.casefold()] = asset_key
    return mapping


def build_name_to_asset_key_from_mvp_characters(
    characters: list[dict[str, Any]],
) -> dict[str, str]:
    """Map character name -> asset key from rankings.json character list."""
    mapping: dict[str, str] = {}
    for character in characters:
        if not isinstance(character, dict):
            continue
        name = str(character.get("name") or "").strip()
        asset_key = str(character.get("characterAssetKey") or "").strip()
        if name and asset_key:
            mapping[name.casefold()] = asset_key
    return mapping


def resolve_snapshot_identity(
    row: SnapshotRow,
    name_to_asset_key: dict[str, str] | None = None,
) -> str:
    asset_key = (row.character_asset_key or "").strip()
    if asset_key:
        return asset_key
    if name_to_asset_key:
        name = (row.character_name or "").strip().casefold()
        if name:
            resolved = name_to_asset_key.get(name)
            if resolved:
                return resolved
    name = (row.character_name or "").strip()
    if name:
        return f"name:{name.casefold()}"
    return ""
