import React from "react";
import FavoriteStar from "./FavoriteStar";
import {
  formatExp,
  formatJobName,
  formatLevelExp,
  gainRankClass,
  GAIN_PERIOD_LABELS,
  getGainAmount,
  topGainersForPeriod,
} from "./rankingUtils";

const PERIODS = ["daily", "weekly", "monthly"];

export default function TopGainHighlights({
  characters,
  selectedId,
  onSelect,
  isFavorite,
  onToggleFavorite,
}) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
      {PERIODS.map((period) => {
        const top = topGainersForPeriod(characters, period, 3);
        return (
          <div
            key={period}
            className="bg-slate-900 border border-slate-800 rounded-xl px-2.5 py-2"
          >
            <h3 className="font-semibold text-xs text-slate-400 mb-1.5">
              {GAIN_PERIOD_LABELS[period]} 増加量 TOP3
            </h3>
            <ul className="space-y-1">
              {top.map((character) => (
                <li key={`${period}-${character.id}`}>
                  <button
                    type="button"
                    onClick={() => onSelect(character.id)}
                    className={`w-full text-left rounded-lg border px-2 py-1.5 transition hover:bg-slate-800/80 ${
                      selectedId === character.id
                        ? "border-cyan-500/70 bg-slate-800/80"
                        : "border-slate-800/80 bg-slate-950/60"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 min-w-0">
                      <div className="flex items-center gap-1 min-w-0">
                        {onToggleFavorite ? (
                          <FavoriteStar
                            active={isFavorite?.(character)}
                            onToggle={() => onToggleFavorite?.(character)}
                            size={14}
                          />
                        ) : null}
                        <span
                          className={`font-bold text-xs shrink-0 ${gainRankClass(character.gainRank)}`}
                        >
                          #{character.gainRank}
                        </span>
                        <span className="font-semibold text-sm truncate">
                          {character.name}
                        </span>
                      </div>
                      <span className="text-emerald-400 text-xs font-semibold shrink-0 tabular-nums">
                        +{formatExp(getGainAmount(character, period))}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-500 truncate mt-0.5 leading-tight pl-5">
                      {formatJobName(character.job)} · レベル順位 #{character.rank} ·{" "}
                      {formatLevelExp(character)}
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        );
      })}
    </div>
  );
}
