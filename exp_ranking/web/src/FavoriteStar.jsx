import React from "react";
import { Star } from "lucide-react";

export default function FavoriteStar({ active, onToggle, size = 18, className = "" }) {
  return (
    <button
      type="button"
      aria-label={active ? "お気に入りを解除" : "お気に入りに追加"}
      title={active ? "お気に入りを解除" : "お気に入りに追加"}
      onClick={(event) => {
        event.stopPropagation();
        onToggle();
      }}
      className={`inline-flex items-center justify-center rounded-lg p-1 transition hover:bg-slate-800/80 ${className}`}
    >
      <Star
        size={size}
        className={
          active
            ? "fill-amber-400 text-amber-400"
            : "text-slate-500 hover:text-amber-300"
        }
      />
    </button>
  );
}
