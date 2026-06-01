import { useCallback, useState } from "react";
import { favoriteKey, loadFavorites, saveFavorites } from "./favorites";

export function useFavorites() {
  const [favorites, setFavorites] = useState(() => loadFavorites());

  const isFavorite = useCallback(
    (character) => favorites.has(favoriteKey(character)),
    [favorites]
  );

  const toggleFavorite = useCallback((character) => {
    const key = favoriteKey(character);
    if (!key) {
      return;
    }
    setFavorites((previous) => {
      const next = new Set(previous);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      saveFavorites(next);
      return next;
    });
  }, []);

  return {
    favorites,
    favoriteCount: favorites.size,
    isFavorite,
    toggleFavorite,
  };
}
