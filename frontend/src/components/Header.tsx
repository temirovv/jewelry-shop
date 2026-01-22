import { memo } from "react";
import { motion } from "framer-motion";
import { ShoppingBag, Search, Menu, Sparkles } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { useCartStore } from "../stores/cartStore";

interface HeaderProps {
  onCartClick?: () => void;
  onMenuClick?: () => void;
  onSearchClick?: () => void;
  transparent?: boolean;
}

export const Header = memo(function Header({
  onCartClick,
  onMenuClick,
  onSearchClick,
  transparent = false,
}: HeaderProps) {
  const itemsCount = useCartStore((state) => state.getItemsCount());

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={`sticky top-0 z-40 w-full transition-all duration-300 ${
        transparent
          ? "bg-transparent"
          : "bg-background/80 backdrop-blur-xl border-b border-border/50"
      }`}
    >
      <div className="flex h-14 items-center justify-between px-4">
        {/* Menu Button */}
        <motion.div whileTap={{ scale: 0.95 }}>
          <Button
            variant="ghost"
            size="icon"
            onClick={onMenuClick}
            className="rounded-xl"
          >
            <Menu className="h-5 w-5" />
          </Button>
        </motion.div>

        {/* Logo */}
        <motion.div
          className="flex items-center gap-1.5"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Sparkles className="w-5 h-5 text-amber-500" />
          <h1 className="text-lg font-display font-bold tracking-tight">
            <span className="gold-text">JEWELRY</span>
          </h1>
        </motion.div>

        {/* Actions */}
        <div className="flex items-center gap-1">
          <motion.div whileTap={{ scale: 0.95 }}>
            <Button
              variant="ghost"
              size="icon"
              onClick={onSearchClick}
              className="rounded-xl"
            >
              <Search className="h-5 w-5" />
            </Button>
          </motion.div>

          <motion.div whileTap={{ scale: 0.95 }} className="relative">
            <Button
              variant="ghost"
              size="icon"
              onClick={onCartClick}
              className="rounded-xl"
            >
              <ShoppingBag className="h-5 w-5" />
            </Button>
            {itemsCount > 0 && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="absolute -top-0.5 -right-0.5"
              >
                <Badge
                  variant="gold"
                  className="h-5 min-w-5 p-0 flex items-center justify-center text-[10px] font-bold shadow-lg"
                >
                  {itemsCount > 9 ? "9+" : itemsCount}
                </Badge>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </motion.header>
  );
});
