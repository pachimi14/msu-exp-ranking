import React from "react";
import FavoriteStar from "./FavoriteStar";
import {
  formatExp,
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
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {PERIODS.map((period) => {
        const top = topGainersForPeriod(characters, period, 3);
        return (
          <div
            key={period}
            className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3"
          >
            <h3 className="font-bold text-sm text-slate-300">
              {GAIN_PERIOD_LABELS[period]} 増加量 TOP3
            </h3>
            <ul className="space-y-2">
              {top.map((character) => (
                <li key={`${period}-${character.id}`}>
                  <button
                    type="button"
                    onClick={() => onSelect(character.id)}
                    className={`w-full text-left rounded-xl border px-3 py-2 transition hover:bg-slate-800/80 ${
                      selectedId === character.id
                        ? "border-cyan-500 bg-slate-800"
                        : "border-slate-800 bg-slate-950"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-1">
                        {onToggleFavorite ? (
                          <FavoriteStar
                            active={isFavorite?.(character)}
                            onToggle={() => onToggleFavorite(character)}
                            size={16}
                          />
                        ) : null}
                        <span className={`font-bold text-sm ${gainRankClass(character.gainRank)}`}>
                          #{character.gainRank}
                        </span>
                      </div>
                      <span className="text-emerald-400 text-sm font-semibold">
                        +{formatExp(getGainAmount(character, period))}
                      </span>
                    </div>
                    <div className="font-semibold truncate mt-1">{character.name}</div>
                    <div className="text-xs text-slate-500">レベル順位 #{character.rank}</div>
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
