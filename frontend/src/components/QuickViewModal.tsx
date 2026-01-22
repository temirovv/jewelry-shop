import { memo, useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import { X, ShoppingBag, Heart, Minus, Plus, ChevronLeft, ChevronRight, Sparkles } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { formatPrice } from "../lib/utils";
import type { Product } from "../types";

interface QuickViewModalProps {
  product: Product | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onAddToCart?: (product: Product, quantity: number) => void;
  onViewDetail?: (product: Product) => void;
}

export const QuickViewModal = memo(function QuickViewModal({
  product,
  open,
  onOpenChange,
  onAddToCart,
  onViewDetail,
}: QuickViewModalProps) {
  const [quantity, setQuantity] = useState(1);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isLiked, setIsLiked] = useState(false);

  // Reset state when product changes or modal opens
  useEffect(() => {
    if (open && product) {
      setQuantity(1);
      setCurrentImageIndex(0);
    }
  }, [open, product?.id]);

  if (!product) return null;

  const images = product.images || [];
  const discount = product.old_price
    ? Math.round(((Number(product.old_price) - Number(product.price)) / Number(product.old_price)) * 100)
    : 0;

  const handleAddToCart = () => {
    onAddToCart?.(product, quantity);
    onOpenChange(false);
  };

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % images.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay asChild>
          <motion.div
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />
        </Dialog.Overlay>
        <Dialog.Content asChild>
          <motion.div
            className="fixed left-1/2 top-1/2 z-50 w-[95vw] max-w-2xl max-h-[90vh] overflow-hidden rounded-2xl bg-background shadow-2xl"
            initial={{ opacity: 0, scale: 0.9, x: "-50%", y: "-45%" }}
            animate={{ opacity: 1, scale: 1, x: "-50%", y: "-50%" }}
            exit={{ opacity: 0, scale: 0.9, x: "-50%", y: "-45%" }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
          >
            <div className="grid md:grid-cols-2 gap-0">
              {/* Image Section */}
              <div className="relative aspect-square md:aspect-auto md:h-full bg-muted">
                <AnimatePresence mode="wait">
                  {images.length > 0 ? (
                    <motion.img
                      key={currentImageIndex}
                      src={images[currentImageIndex]?.image}
                      alt={product.name}
                      className="w-full h-full object-cover"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 0.3 }}
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-50 to-amber-100">
                      <Sparkles className="w-16 h-16 text-amber-400/50" />
                    </div>
                  )}
                </AnimatePresence>

                {/* Image Navigation */}
                {images.length > 1 && (
                  <>
                    <button
                      onClick={prevImage}
                      className="absolute left-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white/80 backdrop-blur-sm shadow-lg hover:bg-white transition-colors"
                    >
                      <ChevronLeft className="w-5 h-5" />
                    </button>
                    <button
                      onClick={nextImage}
                      className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white/80 backdrop-blur-sm shadow-lg hover:bg-white transition-colors"
                    >
                      <ChevronRight className="w-5 h-5" />
                    </button>

                    {/* Dots */}
                    <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-1.5">
                      {images.map((_, idx) => (
                        <button
                          key={idx}
                          onClick={() => setCurrentImageIndex(idx)}
                          className={`w-2 h-2 rounded-full transition-all ${
                            idx === currentImageIndex
                              ? "bg-white w-4"
                              : "bg-white/50"
                          }`}
                        />
                      ))}
                    </div>
                  </>
                )}

                {/* Badges */}
                <div className="absolute top-3 left-3 flex flex-col gap-1.5">
                  {discount > 0 && (
                    <Badge variant="sale">-{discount}%</Badge>
                  )}
                  {product.is_featured && (
                    <Badge variant="gold">
                      <Sparkles className="w-3 h-3 mr-1" />
                      Hit
                    </Badge>
                  )}
                </div>

                {/* Like */}
                <motion.button
                  className="absolute top-3 right-3 p-2.5 rounded-full bg-white/90 backdrop-blur-md shadow-lg"
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setIsLiked(!isLiked)}
                >
                  <Heart
                    className={`w-5 h-5 ${
                      isLiked ? "fill-red-500 text-red-500" : "text-gray-600"
                    }`}
                  />
                </motion.button>
              </div>

              {/* Details Section */}
              <div className="p-6 flex flex-col max-h-[50vh] md:max-h-[90vh] overflow-y-auto">
                {/* Close Button (mobile) */}
                <Dialog.Close asChild>
                  <button className="absolute top-3 right-3 md:hidden p-2 rounded-full bg-muted">
                    <X className="w-4 h-4" />
                  </button>
                </Dialog.Close>

                {/* Category */}
                <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
                  {product.category?.name}
                </p>

                {/* Name */}
                <h2 className="text-xl font-semibold mb-3">{product.name}</h2>

                {/* Price */}
                <div className="flex items-baseline gap-3 mb-4">
                  <span className="text-2xl font-bold gold-text">
                    {formatPrice(Number(product.price))}
                  </span>
                  {product.old_price && (
                    <span className="text-base text-muted-foreground line-through">
                      {formatPrice(Number(product.old_price))}
                    </span>
                  )}
                </div>

                {/* Description */}
                {product.description && (
                  <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                    {product.description}
                  </p>
                )}

                {/* Specs */}
                <div className="grid grid-cols-2 gap-3 mb-6">
                  <div className="p-3 rounded-xl bg-muted/50">
                    <p className="text-xs text-muted-foreground mb-0.5">Vazni</p>
                    <p className="font-medium">{product.weight} gr</p>
                  </div>
                  <div className="p-3 rounded-xl bg-muted/50">
                    <p className="text-xs text-muted-foreground mb-0.5">Metal</p>
                    <p className="font-medium">
                      {product.metal_type === "gold" ? "Oltin 585" :
                       product.metal_type === "silver" ? "Kumush 925" : "Oq oltin 750"}
                    </p>
                  </div>
                  {product.size && (
                    <div className="p-3 rounded-xl bg-muted/50">
                      <p className="text-xs text-muted-foreground mb-0.5">Razmer</p>
                      <p className="font-medium">{product.size}</p>
                    </div>
                  )}
                </div>

                {/* Quantity */}
                <div className="flex items-center gap-4 mb-6">
                  <span className="text-sm font-medium">Miqdori:</span>
                  <div className="flex items-center gap-2">
                    <motion.button
                      whileTap={{ scale: 0.9 }}
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="w-9 h-9 rounded-xl bg-muted flex items-center justify-center hover:bg-muted/80 transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </motion.button>
                    <span className="w-10 text-center font-semibold">{quantity}</span>
                    <motion.button
                      whileTap={{ scale: 0.9 }}
                      onClick={() => setQuantity(quantity + 1)}
                      className="w-9 h-9 rounded-xl bg-muted flex items-center justify-center hover:bg-muted/80 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </motion.button>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-3 mt-auto">
                  <Button
                    variant="gold"
                    size="lg"
                    className="flex-1"
                    onClick={handleAddToCart}
                    disabled={!product.in_stock}
                  >
                    <ShoppingBag className="w-4 h-4 mr-2" />
                    {product.in_stock ? "Savatga qo'shish" : "Sotuvda yo'q"}
                  </Button>
                </div>

                {/* View Full */}
                <button
                  onClick={() => {
                    onViewDetail?.(product);
                    onOpenChange(false);
                  }}
                  className="mt-3 text-sm text-primary hover:underline text-center"
                >
                  To'liq ko'rish →
                </button>

                {/* Close Button (desktop) */}
                <Dialog.Close asChild>
                  <button className="hidden md:flex absolute top-4 right-4 p-2 rounded-full bg-muted hover:bg-muted/80 transition-colors">
                    <X className="w-4 h-4" />
                  </button>
                </Dialog.Close>
              </div>
            </div>
          </motion.div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
});
