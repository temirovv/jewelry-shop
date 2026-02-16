import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product, CartItem } from "../types";
import * as cartApi from "../lib/api/cart";

interface CartState {
  items: CartItem[];
  isOpen: boolean;
  isSyncing: boolean;

  // Actions
  addItem: (product: Product, quantity?: number, size?: string) => void;
  removeItem: (itemId: number) => void;
  updateQuantity: (itemId: number, quantity: number) => void;
  clearCart: () => void;
  openCart: () => void;
  closeCart: () => void;

  // Backend sync
  syncWithBackend: () => Promise<void>;

  // Getters
  getTotal: () => number;
  getItemsCount: () => number;
}

// Backend bilan sinxronizatsiya qilish (xatolikni yutib yuboradi)
async function syncToBackend(
  action: () => Promise<any>
): Promise<CartItem[] | null> {
  try {
    const cart = await action();
    return cart.items || [];
  } catch {
    return null;
  }
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      isOpen: false,
      isSyncing: false,

      addItem: (product, quantity = 1, size) => {
        const items = get().items;
        const existingItem = items.find(
          (item) => item.product.id === product.id && item.size === size
        );

        if (existingItem) {
          set({
            items: items.map((item) =>
              item.id === existingItem.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
          });
        } else {
          const newItem: CartItem = {
            id: Date.now(),
            product,
            quantity,
            size,
          };
          set({ items: [...items, newItem] });
        }

        // Backend ga sinxronlash (background)
        syncToBackend(() => cartApi.addToCart(product.id, quantity, size || ""))
          .then((backendItems) => {
            if (backendItems) set({ items: backendItems });
          });
      },

      removeItem: (itemId) => {
        const item = get().items.find((i) => i.id === itemId);
        set({ items: get().items.filter((i) => i.id !== itemId) });

        if (item) {
          syncToBackend(() => cartApi.removeCartItem(itemId))
            .then((backendItems) => {
              if (backendItems) set({ items: backendItems });
            });
        }
      },

      updateQuantity: (itemId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(itemId);
          return;
        }
        set({
          items: get().items.map((item) =>
            item.id === itemId ? { ...item, quantity } : item
          ),
        });

        syncToBackend(() => cartApi.updateCartItem(itemId, quantity))
          .then((backendItems) => {
            if (backendItems) set({ items: backendItems });
          });
      },

      clearCart: () => {
        set({ items: [] });
        syncToBackend(() => cartApi.clearCartApi());
      },

      openCart: () => set({ isOpen: true }),
      closeCart: () => set({ isOpen: false }),

      syncWithBackend: async () => {
        set({ isSyncing: true });
        try {
          const cart = await cartApi.getCart();
          if (cart.items && cart.items.length > 0) {
            set({ items: cart.items });
          } else {
            // Backend bo'sh — local items ni backend ga yuborish
            const localItems = get().items;
            for (const item of localItems) {
              try {
                await cartApi.addToCart(
                  item.product.id,
                  item.quantity,
                  item.size || ""
                );
              } catch {
                // skip
              }
            }
            // Qayta olish
            if (localItems.length > 0) {
              const updated = await cartApi.getCart();
              if (updated.items && updated.items.length > 0) {
                set({ items: updated.items });
              }
            }
          }
        } catch {
          // Offline — localStorage dan foydalanish
        } finally {
          set({ isSyncing: false });
        }
      },

      getTotal: () =>
        get().items.reduce(
          (total, item) => total + Number(item.product.price) * item.quantity,
          0
        ),

      getItemsCount: () =>
        get().items.reduce((count, item) => count + item.quantity, 0),
    }),
    {
      name: "jewelry-cart",
      partialize: (state) => ({ items: state.items }),
    }
  )
);
