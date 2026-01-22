import { memo } from "react";
import { motion } from "framer-motion";
import { Home, Search, Heart, ShoppingBag, User } from "lucide-react";
import { useCartStore } from "../stores/cartStore";

type TabType = "home" | "search" | "favorites" | "cart" | "profile";

interface BottomNavProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

const tabs = [
  { id: "home" as TabType, icon: Home, label: "Bosh sahifa" },
  { id: "search" as TabType, icon: Search, label: "Qidirish" },
  { id: "favorites" as TabType, icon: Heart, label: "Sevimli" },
  { id: "cart" as TabType, icon: ShoppingBag, label: "Savat" },
  { id: "profile" as TabType, icon: User, label: "Profil" },
];

export const BottomNav = memo(function BottomNav({
  activeTab,
  onTabChange,
}: BottomNavProps) {
  const itemsCount = useCartStore((state) => state.getItemsCount());

  return (
    <motion.nav
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      transition={{ type: "spring", damping: 25, stiffness: 300 }}
      className="fixed bottom-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-t border-border/50 safe-area-bottom"
    >
      <div className="flex items-center justify-around h-16 px-2">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          const showBadge = tab.id === "cart" && itemsCount > 0;

          return (
            <motion.button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className="relative flex flex-col items-center justify-center w-16 h-14 rounded-2xl"
              whileTap={{ scale: 0.9 }}
            >
              {/* Active Background */}
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-1 rounded-2xl gold-gradient opacity-10"
                  transition={{ type: "spring", damping: 25, stiffness: 300 }}
                />
              )}

              {/* Icon */}
              <motion.div
                animate={{
                  scale: isActive ? 1.1 : 1,
                  y: isActive ? -2 : 0,
                }}
                transition={{ type: "spring", damping: 20, stiffness: 300 }}
                className="relative"
              >
                <Icon
                  className={`w-5 h-5 transition-colors ${
                    isActive ? "text-primary" : "text-muted-foreground"
                  }`}
                  strokeWidth={isActive ? 2.5 : 2}
                />

                {/* Badge */}
                {showBadge && (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1.5 -right-1.5 w-4 h-4 rounded-full gold-gradient text-[10px] font-bold text-white flex items-center justify-center shadow-lg"
                  >
                    {itemsCount > 9 ? "9" : itemsCount}
                  </motion.span>
                )}
              </motion.div>

              {/* Label */}
              <motion.span
                animate={{
                  opacity: isActive ? 1 : 0.6,
                  y: isActive ? 0 : 2,
                }}
                className={`text-[10px] mt-1 font-medium transition-colors ${
                  isActive ? "text-primary" : "text-muted-foreground"
                }`}
              >
                {tab.label}
              </motion.span>
            </motion.button>
          );
        })}
      </div>
    </motion.nav>
  );
});
