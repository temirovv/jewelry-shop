import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Heart, Trash2, ShoppingBag } from "lucide-react";
import { Button } from "../components/ui/button";
import { ProductCard } from "../components/ProductCard";
import { BottomNav } from "../components/BottomNav";
import { CartSheet } from "../components/CartSheet";
import { useFavoritesStore } from "../stores/favoritesStore";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { useState } from "react";
import type { Product } from "../types";

export function FavoritesPage() {
  const navigate = useNavigate();
  const [cartOpen, setCartOpen] = useState(false);

  const items = useFavoritesStore((state) => state.items);
  const clearAll = useFavoritesStore((state) => state.clearAll);
  const addItem = useCartStore((state) => state.addItem);
  const { hapticFeedback } = useTelegram();

  const handleAddToCart = useCallback(
    (product: Product, quantity: number = 1) => {
      addItem(product, quantity);
      hapticFeedback?.impactOccurred?.("medium");
      toast.success(`"${product.name}" savatga qo'shildi`);
    },
    [addItem, hapticFeedback]
  );

  const handleProductPress = useCallback(
    (product: Product) => {
      hapticFeedback?.impactOccurred?.("light");
      navigate(`/product/${product.id}`);
    },
    [hapticFeedback, navigate]
  );

  const handleClearAll = () => {
    if (items.length === 0) return;
    clearAll();
    hapticFeedback?.notificationOccurred?.("warning");
    toast.info("Sevimlilar tozalandi");
  };

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2">
            <Heart className="w-5 h-5 text-primary" />
            <h1 className="text-lg font-semibold">Sevimlilar</h1>
          </div>
          {items.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClearAll}
              className="text-muted-foreground"
            >
              <Trash2 className="w-4 h-4 mr-1" />
              Tozalash
            </Button>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="px-4 py-4">
        <AnimatePresence mode="wait">
          {items.length === 0 ? (
            <motion.div
              key="empty"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="text-center py-20"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", damping: 15, delay: 0.1 }}
                className="w-24 h-24 rounded-full bg-muted flex items-center justify-center mx-auto mb-6"
              >
                <Heart className="w-12 h-12 text-muted-foreground" />
              </motion.div>
              <h3 className="font-semibold text-lg mb-2">
                Sevimlilar bo'sh
              </h3>
              <p className="text-muted-foreground mb-6">
                Mahsulotlardagi yurak belgisini bosib saqlang
              </p>
              <Button onClick={() => navigate("/")} className="gold-gradient">
                <ShoppingBag className="w-4 h-4 mr-2" />
                Xarid qilish
              </Button>
            </motion.div>
          ) : (
            <motion.div
              key="items"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <p className="text-sm text-muted-foreground mb-4">
                {items.length} ta mahsulot
              </p>
              <div className="grid grid-cols-2 gap-3">
                {items.map((product, index) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    index={index}
                    onPress={handleProductPress}
                    onAddToCart={handleAddToCart}
                    onQuickView={handleProductPress}
                  />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Bottom Navigation */}
      <BottomNav
        activeTab="favorites"
        onTabChange={(tab) => {
          if (tab === "cart") setCartOpen(true);
          else if (tab === "home") navigate("/");
          else if (tab === "search") navigate("/search");
          else if (tab === "profile") navigate("/profile");
        }}
      />

      {/* Cart Sheet */}
      <CartSheet
        open={cartOpen}
        onOpenChange={setCartOpen}
        onCheckout={() => {
          setCartOpen(false);
          navigate("/checkout");
        }}
      />
    </div>
  );
}
