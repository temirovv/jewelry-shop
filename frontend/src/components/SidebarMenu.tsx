import { memo } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Home,
  Search,
  Heart,
  ShoppingBag,
  User,
  Package,
  Phone,
  Info,
  Sparkles,
  ChevronRight,
} from "lucide-react";
import { useTelegram } from "../hooks/useTelegram";
import { useCartStore } from "../stores/cartStore";
import { useFavoritesStore } from "../stores/favoritesStore";
import { springs, staggerContainerVariants, staggerItemVariants } from "../lib/animations";

interface SidebarMenuProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const menuItems = [
  { icon: Home, label: "Bosh sahifa", path: "/" },
  { icon: Search, label: "Qidirish", path: "/search" },
  { icon: Heart, label: "Sevimlilar", path: "/favorites", badge: "favorites" },
  { icon: ShoppingBag, label: "Savat", path: "/cart", badge: "cart" },
  { icon: Package, label: "Buyurtmalarim", path: "/profile" },
  { icon: User, label: "Profil", path: "/profile" },
];

const bottomItems = [
  { icon: Phone, label: "Bog'lanish", action: "contact" },
  { icon: Info, label: "Biz haqimizda", action: "about" },
];

export const SidebarMenu = memo(function SidebarMenu({
  open,
  onOpenChange,
}: SidebarMenuProps) {
  const navigate = useNavigate();
  const { user, hapticFeedback } = useTelegram();
  const cartCount = useCartStore((state) => state.getItemsCount());
  const favoritesCount = useFavoritesStore((state) => state.items.length);

  const handleNavigate = (path: string) => {
    hapticFeedback?.impactOccurred?.("light");
    onOpenChange(false);
    setTimeout(() => navigate(path), 150);
  };

  const handleAction = (action: string) => {
    hapticFeedback?.impactOccurred?.("light");
    if (action === "contact") {
      window.open("https://t.me/jewelry_support", "_blank");
    }
    onOpenChange(false);
  };

  const getBadgeCount = (badge?: string) => {
    if (badge === "cart") return cartCount;
    if (badge === "favorites") return favoritesCount;
    return 0;
  };

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={() => onOpenChange(false)}
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
          />

          {/* Sidebar */}
          <motion.div
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ ...springs.smooth }}
            className="fixed left-0 top-0 bottom-0 z-50 w-[280px] bg-background shadow-2xl flex flex-col"
          >
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, ...springs.smooth }}
              className="p-4 border-b border-border/50"
            >
              <div className="flex items-center justify-between mb-4">
                <motion.div
                  className="flex items-center gap-2"
                  whileHover={{ scale: 1.02 }}
                >
                  <Sparkles className="w-6 h-6 text-amber-500" />
                  <span className="text-xl font-display font-bold gold-text">
                    JEWELRY
                  </span>
                </motion.div>
                <motion.button
                  onClick={() => onOpenChange(false)}
                  className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center"
                  whileTap={{ scale: 0.9 }}
                  whileHover={{ scale: 1.05 }}
                >
                  <X className="w-5 h-5" />
                </motion.button>
              </div>

              {/* User info */}
              {user && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.15, ...springs.smooth }}
                  className="flex items-center gap-3 p-3 rounded-xl bg-muted/50"
                >
                  <div className="w-12 h-12 rounded-full gold-gradient flex items-center justify-center text-white font-bold shadow-lg">
                    {user.first_name[0]}
                  </div>
                  <div>
                    <p className="font-medium">
                      {user.first_name} {user.last_name}
                    </p>
                    {user.username && (
                      <p className="text-sm text-muted-foreground">
                        @{user.username}
                      </p>
                    )}
                  </div>
                </motion.div>
              )}
            </motion.div>

            {/* Menu Items */}
            <motion.nav
              className="flex-1 p-4 space-y-1 overflow-y-auto"
              variants={staggerContainerVariants}
              initial="hidden"
              animate="visible"
            >
              {menuItems.map((item, index) => {
                const Icon = item.icon;
                const badgeCount = getBadgeCount(item.badge);
                return (
                  <motion.button
                    key={item.path + item.label}
                    variants={staggerItemVariants}
                    custom={index}
                    whileTap={{ scale: 0.98, x: 4 }}
                    whileHover={{ x: 4, backgroundColor: "rgba(0,0,0,0.05)" }}
                    onClick={() => handleNavigate(item.path)}
                    className="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-colors text-left"
                  >
                    <Icon className="w-5 h-5 text-muted-foreground" />
                    <span className="flex-1 font-medium">{item.label}</span>
                    {badgeCount > 0 && (
                      <motion.span
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-6 h-6 rounded-full gold-gradient text-white text-xs font-bold flex items-center justify-center shadow-md"
                      >
                        {badgeCount > 9 ? "9+" : badgeCount}
                      </motion.span>
                    )}
                    <ChevronRight className="w-4 h-4 text-muted-foreground/50" />
                  </motion.button>
                );
              })}
            </motion.nav>

            {/* Bottom Items */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, ...springs.smooth }}
              className="p-4 border-t border-border/50 space-y-1"
            >
              {bottomItems.map((item) => {
                const Icon = item.icon;
                return (
                  <motion.button
                    key={item.action}
                    whileTap={{ scale: 0.98 }}
                    whileHover={{ x: 4 }}
                    onClick={() => handleAction(item.action)}
                    className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-muted transition-colors text-left text-muted-foreground"
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </motion.button>
                );
              })}
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
});
