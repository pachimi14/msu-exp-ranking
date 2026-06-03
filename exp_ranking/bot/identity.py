"""Stable character identity across ranking days (asset key + name fallback)."""

from __future__ import annotations

from models import SnapshotRow


def build_name_to_asset_key(snapshots: list[SnapshotRow]) -> dict[str, str]:
    """Map character name -> asset key using any snapshot row that has a key."""
    mapping: dict[str, str] = {}
    for row in snapshots:
        asset_key = (row.character_asset_key or "").strip()
        name = (row.character_name or "").strip()
        if asset_key and name:
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
