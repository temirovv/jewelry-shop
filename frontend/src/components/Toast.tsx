import { memo, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, XCircle, AlertCircle, X } from "lucide-react";
import { create } from "zustand";

// Toast types
type ToastType = "success" | "error" | "info";

interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

interface ToastState {
  toasts: Toast[];
  addToast: (message: string, type?: ToastType) => void;
  removeToast: (id: number) => void;
}

// Toast store
export const useToastStore = create<ToastState>((set, get) => ({
  toasts: [],
  addToast: (message, type = "success") => {
    const id = Date.now();
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

// Toast container component
export const ToastContainer = memo(function ToastContainer() {
  const toasts = useToastStore((state) => state.toasts);
  const removeToast = useToastStore((state) => state.removeToast);

  return (
    <div className="fixed top-4 right-4 left-4 sm:left-auto sm:w-96 z-[100] flex flex-col gap-2">
      <AnimatePresence mode="popLayout">
        {toasts.map((toastItem) => (
          <ToastItem
            key={toastItem.id}
            toast={toastItem}
            onClose={() => removeToast(toastItem.id)}
          />
        ))}
      </AnimatePresence>
    </div>
  );
});

interface ToastItemProps {
  toast: Toast;
  onClose: () => void;
}

const ToastItem = memo(function ToastItem({ toast, onClose }: ToastItemProps) {
  const icons = {
    success: CheckCircle,
    error: XCircle,
    info: AlertCircle,
  };

  const colors = {
    success: "bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-200",
    error: "bg-red-50 border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-800 dark:text-red-200",
    info: "bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-200",
  };

  const iconColors = {
    success: "text-green-500",
    error: "text-red-500",
    info: "text-blue-500",
  };

  const Icon = icons[toast.type];

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, x: 100, scale: 0.95 }}
      transition={{ duration: 0.2 }}
      className={`flex items-center gap-3 p-4 rounded-xl border shadow-lg backdrop-blur-sm ${colors[toast.type]}`}
    >
      <Icon className={`w-5 h-5 flex-shrink-0 ${iconColors[toast.type]}`} />
      <p className="flex-1 text-sm font-medium">{toast.message}</p>
      <button
        onClick={onClose}
        className="p-1 rounded-lg hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
      >
        <X className="w-4 h-4" />
      </button>
    </motion.div>
  );
});
