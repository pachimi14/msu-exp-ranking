const STORAGE_KEY = "msu_exp_ranking_favorites";

/** Stable id across JSON re-exports (display id in list may change). */
export function favoriteKey(character) {
  return String(character?.name ?? "").trim();
}

export function loadFavorites() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = JSON.parse(raw || "[]");
    if (!Array.isArray(parsed)) {
      return new Set();
    }
    return new Set(parsed.filter((item) => typeof item === "string" && item));
  } catch {
    return new Set();
  }
}

export function saveFavorites(favorites) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...favorites]));
}
