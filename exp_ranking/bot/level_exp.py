"""Level-up EXP table and calculations for MSU ranking."""

from __future__ import annotations

# MSU: EXP required to reach the next level (Lv225-Lv249)
_EXP_TO_NEXT_LEVEL_225_249: dict[int, int] = {
    225: 314_754_893_173,
    226: 327_345_088_899,
    227: 340_438_892_454,
    228: 354_056_448_150,
    229: 368_218_706_074,
    230: 751_166_160_390,
    231: 766_189_483_595,
    232: 781_513_273_265,
    233: 797_143_538_730,
    234: 813_086_409_503,
    235: 829_348_137_691,
    236: 845_935_100_443,
    237: 862_853_802_451,
    238: 880_110_878_499,
    239: 897_713_096_067,
    240: 1_813_380_454_053,
    241: 1_831_514_258_591,
    242: 1_849_829_401_175,
    243: 1_868_327_695_184,
    244: 1_887_010_972_134,
    245: 1_905_881_081_854,
    246: 1_924_939_892_669,
    247: 1_944_189_291_594,
    248: 1_963_631_184_509,
    249: 1_983_267_496_351,
}

EXP_TO_NEXT_LEVEL: dict[int, int] = dict(_EXP_TO_NEXT_LEVEL_225_249)

TABLE_MIN_LEVEL = 225
TABLE_MAX_LEVEL = 249
MAX_RANKING_LEVEL = 250

MIN_RANKING_LEVEL = TABLE_MIN_LEVEL

TARGET_TOTAL_EXP_250: int = sum(
    EXP_TO_NEXT_LEVEL[level] for level in range(240, 250)
)

TOTAL_EXP_225_TO_250: int = sum(
    EXP_TO_NEXT_LEVEL[level] for level in range(TABLE_MIN_LEVEL, 250)
)


def exp_required_for_level(level: int) -> int | None:
    if level >= MAX_RANKING_LEVEL:
        return None
    return EXP_TO_NEXT_LEVEL.get(level)


def calculate_level_exp_percent(level: int, exp: int) -> float:
    """Progress within the current level (0-100), matching in-game ranking display."""
    if level >= MAX_RANKING_LEVEL:
        return 100.0

    required = exp_required_for_level(level)
    if not required or required <= 0:
        return 0.0

    percent = exp / required * 100.0
    return round(min(max(percent, 0.0), 100.0), 3)


def calculate_exp_to_250(level: int, exp: int) -> int:
    if level >= MAX_RANKING_LEVEL:
        return 0

    required_current = exp_required_for_level(level)
    if required_current is None:
        return 0

    remaining = max(required_current - exp, 0)
    for lv in range(level + 1, MAX_RANKING_LEVEL):
        remaining += EXP_TO_NEXT_LEVEL.get(lv, 0)
    return remaining


def calculate_total_exp_from_240(level: int, exp: int) -> int:
    """Cumulative EXP from Lv240 start (for 240+ daily gain / analysis)."""
    if level >= MAX_RANKING_LEVEL:
        return TARGET_TOTAL_EXP_250
    if level < 240:
        return 0

    total = exp
    for lv in range(240, level):
        total += EXP_TO_NEXT_LEVEL[lv]
    return total


def calculate_progress_toward_250(level: int, exp: int) -> int:
    """Monotonic progress value toward Lv250 (daily gain for all ranked levels)."""
    if level >= MAX_RANKING_LEVEL:
        return TOTAL_EXP_225_TO_250
    if level < TABLE_MIN_LEVEL:
        return 0
    return TOTAL_EXP_225_TO_250 - calculate_exp_to_250(level, exp)


def calculate_exp_percent(level: int, exp: int) -> float:
    return calculate_level_exp_percent(level, exp)
