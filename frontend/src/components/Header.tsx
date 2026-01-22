import { ShoppingBag, Search, Menu } from "lucide-react";
import { motion } from "framer-motion";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { useCartStore } from "../stores/cartStore";

interface HeaderProps {
  onCartClick?: () => void;
  onMenuClick?: () => void;
  onSearchClick?: () => void;
}

export function Header({ onCartClick, onMenuClick, onSearchClick }: HeaderProps) {
  const itemsCount = useCartStore((state) => state.getItemsCount());

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    >
      <div className="container flex h-14 items-center justify-between px-4">
        {/* Menu Button */}
        <Button variant="ghost" size="icon" onClick={onMenuClick}>
          <Menu className="h-5 w-5" />
        </Button>

        {/* Logo */}
        <div className="flex items-center gap-2">
          <h1 className="text-lg font-display font-bold gold-text">
            JEWELRY
          </h1>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" onClick={onSearchClick}>
            <Search className="h-5 w-5" />
          </Button>

          <Button
            variant="ghost"
            size="icon"
            className="relative"
            onClick={onCartClick}
          >
            <ShoppingBag className="h-5 w-5" />
            {itemsCount > 0 && (
              <Badge
                variant="gold"
                className="absolute -top-1 -right-1 h-5 w-5 p-0 flex items-center justify-center text-[10px]"
              >
                {itemsCount > 9 ? "9+" : itemsCount}
              </Badge>
            )}
          </Button>
        </div>
      </div>
    </motion.header>
  );
}
