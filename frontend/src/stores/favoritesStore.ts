import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product } from "../types";
import * as favoritesApi from "../lib/api/favorites";

interface FavoritesState {
  items: Product[];
  isSyncing: boolean;

  addItem: (product: Product) => void;
  removeItem: (productId: number) => void;
  toggleItem: (product: Product) => void;
  isFavorite: (productId: number) => boolean;
  clearAll: () => void;

  syncWithBackend: () => Promise<void>;
}

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set, get) => ({
      items: [],
      isSyncing: false,

      addItem: (product) => {
        const items = get().items;
        if (items.find((item) => item.id === product.id)) return;
        set({ items: [...items, product] });

        favoritesApi.toggleFavorite(product.id).catch(() => {
          set({ items: get().items.filter((i) => i.id !== product.id) });
        });
      },

      removeItem: (productId) => {
        const prev = get().items;
        set({ items: prev.filter((item) => item.id !== productId) });

        favoritesApi.toggleFavorite(productId).catch(() => {
          set({ items: prev });
        });
      },

      toggleItem: (product) => {
        const items = get().items;
        const exists = items.some((item) => item.id === product.id);
        if (exists) {
          get().removeItem(product.id);
        } else {
          get().addItem(product);
        }
      },

      isFavorite: (productId) =>
        get().items.some((item) => item.id === productId),

      clearAll: () => {
        const prev = get().items;
        set({ items: [] });
        favoritesApi.clearFavoritesApi().catch(() => {
          set({ items: prev });
        });
      },

      syncWithBackend: async () => {
        set({ isSyncing: true });
        try {
          const remote = await favoritesApi.getFavorites();
          const remoteIds = new Set(remote.map((r) => r.product.id));
          const localItems = get().items;

          // Local-only yozuvlarni backend'ga yuklash (merge)
          for (const item of localItems) {
            if (!remoteIds.has(item.id)) {
              try {
                await favoritesApi.toggleFavorite(item.id);
              } catch {
                // skip
              }
            }
          }

          // Yakuniy ro'yxatni olish
          const merged = await favoritesApi.getFavorites();
          set({ items: merged.map((r) => r.product) });
        } catch {
          // offline — localStorage qoladi
        } finally {
          set({ isSyncing: false });
        }
      },
    }),
    {
      name: "ziyora-favorites",
      partialize: (state) => ({ items: state.items }),
    },
  ),
);
