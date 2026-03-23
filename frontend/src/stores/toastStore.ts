import { create } from "zustand";

// Toast types
export type ToastType = "success" | "error" | "info";

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

interface ToastState {
  toasts: Toast[];
  addToast: (message: string, type?: ToastType) => void;
  removeToast: (id: number) => void;
}

let _toastCounter = 0;

// Toast store
export const useToastStore = create<ToastState>((set, get) => ({
  toasts: [],
  addToast: (message, type = "success") => {
    const id = ++_toastCounter;
    set({ toasts: [...get().toasts, { id, message, type }] });

    // Auto remove after 3 seconds
    setTimeout(() => {
      get().removeToast(id);
    }, 3000);
  },
  removeToast: (id) => {
    set({ toasts: get().toasts.filter((t) => t.id !== id) });
  },
}));

// Helper function for easy use
export const toast = {
  success: (message: string) => useToastStore.getState().addToast(message, "success"),
  error: (message: string) => useToastStore.getState().addToast(message, "error"),
  info: (message: string) => useToastStore.getState().addToast(message, "info"),
};
