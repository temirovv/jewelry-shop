import { memo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Home, Search, Heart, ShoppingBag, User } from "lucide-react";
import { useCartStore } from "../stores/cartStore";
import { useFavoritesStore } from "../stores/favoritesStore";

type TabType = "home" | "search" | "favorites" | "cart" | "profile";

interface BottomNavProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

const tabs = [
  { id: "home" as TabType, icon: Home, label: "Bosh sahifa" },
  { id: "search" as TabType, icon: Search, label: "Qidirish" },
  { id: "favorites" as TabType, icon: Heart, label: "Sevimli", badge: "favorites" },
  { id: "cart" as TabType, icon: ShoppingBag, label: "Savat", badge: "cart" },
  { id: "profile" as TabType, icon: User, label: "Profil" },
];

export const BottomNav = memo(function BottomNav({
  activeTab,
  onTabChange,
}: BottomNavProps) {
  const cartCount = useCartStore((state) => state.getItemsCount());
  const favoritesCount = useFavoritesStore((state) => state.items.length);

  const getBadgeCount = (badge?: string) => {
    if (badge === "cart") return cartCount;
    if (badge === "favorites") return favoritesCount;
    return 0;
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-background/90 backdrop-blur-xl border-t border-border/50 safe-area-bottom">
      <div className="flex items-center justify-around h-16 px-2">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          const badgeCount = getBadgeCount(tab.badge);

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className="relative flex flex-col items-center justify-center w-16 h-14 rounded-2xl active:scale-95 transition-transform duration-150"
            >
              {/* Active Background - silliq layoutId animatsiya */}
              {isActive && (
                <motion.div
                  layoutId="navActiveTab"
                  className="absolute inset-1 rounded-2xl bg-primary/10"
                  transition={{
                    type: "spring",
                    stiffness: 380,
                    damping: 30,
                  }}
                />
              )}

              {/* Icon */}
              <div className="relative">
                <Icon
                  className={`w-5 h-5 transition-all duration-200 ${
                    isActive
                      ? "text-primary scale-110"
                      : "text-muted-foreground"
                  }`}
                  strokeWidth={isActive ? 2.5 : 2}
                />

                {/* Badge */}
                <AnimatePresence mode="wait">
                  {badgeCount > 0 && (
                    <motion.span
                      key={badgeCount}
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      exit={{ scale: 0, opacity: 0 }}
                      transition={{ type: "spring", stiffness: 500, damping: 20 }}
                      className="absolute -top-1.5 -right-2 min-w-4 h-4 px-1 rounded-full gold-gradient text-[10px] font-bold text-white flex items-center justify-center shadow-md"
                    >
                      {badgeCount > 9 ? "9+" : badgeCount}
                    </motion.span>
                  )}
                </AnimatePresence>
              </div>

              {/* Label */}
              <span
                className={`text-[10px] mt-1 font-medium transition-all duration-200 ${
                  isActive
                    ? "text-primary"
                    : "text-muted-foreground opacity-70"
                }`}
              >
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
});
