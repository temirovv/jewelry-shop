import { memo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Minus, Plus, Trash2, ShoppingBag, Sparkles } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "./ui/sheet";
import { Button } from "./ui/button";
import { useCartStore } from "../stores/cartStore";
import { formatPrice } from "../lib/utils";
import type { CartItem } from "../types";

interface CartSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCheckout?: () => void;
}

export const CartSheet = memo(function CartSheet({
  open,
  onOpenChange,
  onCheckout,
}: CartSheetProps) {
  const { items, updateQuantity, removeItem, getTotal, getItemsCount } = useCartStore();
  const total = getTotal();
  const itemsCount = getItemsCount();

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="w-full sm:max-w-md flex flex-col !p-0">
        <SheetHeader className="px-5 pt-5 pb-0">
          <SheetTitle className="flex items-center gap-2">
            <ShoppingBag className="w-5 h-5" />
            Savat
            {itemsCount > 0 && (
              <span className="text-sm font-normal text-muted-foreground">
                ({itemsCount} ta)
              </span>
            )}
          </SheetTitle>
        </SheetHeader>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto px-5 py-4">
          {items.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col items-center justify-center h-full text-center"
            >
              <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mb-4">
                <ShoppingBag className="w-10 h-10 text-muted-foreground" />
              </div>
              <h3 className="font-medium mb-1">Savat bo'sh</h3>
              <p className="text-sm text-muted-foreground">
                Mahsulotlarni savatga qo'shing
              </p>
            </motion.div>
          ) : (
            <AnimatePresence mode="popLayout">
              {items.map((item, index) => (
                <CartItemCard
                  key={item.id}
                  item={item}
                  index={index}
                  onUpdateQuantity={updateQuantity}
                  onRemove={removeItem}
                />
              ))}
            </AnimatePresence>
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && (
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="border-t bg-card p-5 space-y-4"
          >
            {/* Summary */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Mahsulotlar ({itemsCount})</span>
                <span>{formatPrice(total)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Yetkazib berish</span>
                <span className="text-green-600">Bepul</span>
              </div>
              <div className="h-px bg-border my-2" />
              <div className="flex justify-between items-center">
                <span className="font-medium">Jami</span>
                <span className="text-xl font-bold gold-text">{formatPrice(total)}</span>
              </div>
            </div>

            {/* Checkout Button */}
            <Button
              variant="gold"
              size="lg"
              className="w-full text-base"
              onClick={onCheckout}
            >
              <Sparkles className="w-4 h-4 mr-2" />
              Buyurtma berish
            </Button>
          </motion.div>
        )}
      </SheetContent>
    </Sheet>
  );
});

interface CartItemCardProps {
  item: CartItem;
  index: number;
  onUpdateQuantity: (id: number, quantity: number) => void;
  onRemove: (id: number) => void;
}

const CartItemCard = memo(function CartItemCard({
  item,
  index,
  onUpdateQuantity,
  onRemove,
}: CartItemCardProps) {
  const mainImage = item.product.images?.find((img) => img.is_main) || item.product.images?.[0];

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20, height: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="flex gap-3 py-4 border-b last:border-0"
    >
      {/* Image */}
      <div className="w-20 h-20 rounded-xl overflow-hidden bg-muted flex-shrink-0">
        {mainImage?.image ? (
          <img
            src={mainImage.image}
            alt={item.product.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-50 to-amber-100">
            <Sparkles className="w-6 h-6 text-amber-400/50" />
          </div>
        )}
      </div>

      {/* Details */}
      <div className="flex-1 min-w-0">
        <h4 className="font-medium text-sm line-clamp-2 mb-1">
          {item.product.name}
        </h4>
        {item.size && (
          <p className="text-xs text-muted-foreground mb-1">
            Razmer: {item.size}
          </p>
        )}
        <p className="font-semibold text-sm gold-text">
          {formatPrice(Number(item.product.price))}
        </p>

        {/* Quantity Controls */}
        <div className="flex items-center justify-between mt-2">
          <div className="flex items-center gap-1">
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
              className="w-7 h-7 rounded-lg bg-muted flex items-center justify-center hover:bg-muted/80 transition-colors"
            >
              <Minus className="w-3.5 h-3.5" />
            </motion.button>
            <span className="w-8 text-center text-sm font-medium">
              {item.quantity}
            </span>
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
              className="w-7 h-7 rounded-lg bg-muted flex items-center justify-center hover:bg-muted/80 transition-colors"
            >
              <Plus className="w-3.5 h-3.5" />
            </motion.button>
          </div>

          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => onRemove(item.id)}
            className="p-2 text-muted-foreground hover:text-destructive transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
});
