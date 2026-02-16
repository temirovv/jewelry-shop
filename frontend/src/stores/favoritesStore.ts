import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product } from "../types";

interface FavoritesState {
  items: Product[];
  addItem: (product: Product) => void;
  removeItem: (productId: number) => void;
  toggleItem: (product: Product) => void;
  isFavorite: (productId: number) => boolean;
  clearAll: () => void;
}

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product) => {
        const items = get().items;
        if (!items.find((item) => item.id === product.id)) {
          set({ items: [...items, product] });
        }
      },

      removeItem: (productId) => {
        set({ items: get().items.filter((item) => item.id !== productId) });
      },

      toggleItem: (product) => {
        const items = get().items;
        const exists = items.find((item) => item.id === product.id);
        if (exists) {
          set({ items: items.filter((item) => item.id !== product.id) });
        } else {
          set({ items: [...items, product] });
        }
      },

      isFavorite: (productId) => {
        return get().items.some((item) => item.id === productId);
      },

      clearAll: () => set({ items: [] }),
    }),
    {
      name: "jewelry-favorites",
    }
  )
);
