import { memo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Heart, ShoppingBag, Eye, Sparkles } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Skeleton } from "./ui/skeleton";
import { formatPrice } from "../lib/utils";
import { springs, easings } from "../lib/animations";
import { useFavoritesStore } from "../stores/favoritesStore";
import type { Product } from "../types";

interface ProductCardProps {
  product: Product;
  index?: number;
  onPress?: (product: Product) => void;
  onAddToCart?: (product: Product) => void;
  onQuickView?: (product: Product) => void;
}

export const ProductCard = memo(function ProductCard({
  product,
  index = 0,
  onPress,
  onAddToCart,
  onQuickView,
}: ProductCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const { toggleItem, isFavorite } = useFavoritesStore();
  const isLiked = isFavorite(product.id);

  const mainImage = product.images?.find((img) => img.is_main) || product.images?.[0];
  const discount = product.old_price
    ? Math.round(((Number(product.old_price) - Number(product.price)) / Number(product.old_price)) * 100)
    : 0;

  const handleLike = (e: React.MouseEvent) => {
    e.stopPropagation();
    toggleItem(product);
  };

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAddToCart?.(product);
  };

  const handleQuickView = (e: React.MouseEvent) => {
    e.stopPropagation();
    onQuickView?.(product);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{
        delay: index * 0.04,
        ...springs.smooth,
      }}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
    >
      <Card
        className="overflow-hidden cursor-pointer group border-0 shadow-sm hover:shadow-xl transition-shadow duration-500 bg-card/80 backdrop-blur-sm"
        onClick={() => onPress?.(product)}
      >
        {/* Image Container */}
        <div className="relative aspect-square overflow-hidden bg-gradient-to-br from-muted/50 to-muted">
          {/* Skeleton while loading */}
          <AnimatePresence>
            {!imageLoaded && mainImage?.image && (
              <motion.div
                exit={{ opacity: 0 }}
                className="absolute inset-0"
              >
                <Skeleton className="w-full h-full" />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Product Image */}
          {mainImage?.image ? (
            <motion.img
              src={mainImage.image}
              alt={product.name}
              className="w-full h-full object-cover"
              initial={{ opacity: 0, scale: 1.1 }}
              animate={{
                opacity: imageLoaded ? 1 : 0,
                scale: isHovered ? 1.06 : 1,
              }}
              transition={{
                opacity: { duration: 0.4 },
                scale: { duration: 0.5, ease: easings.luxury },
              }}
              onLoad={() => setImageLoaded(true)}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900/20 dark:to-amber-800/20">
              <Sparkles className="w-12 h-12 text-amber-400/50" />
            </div>
          )}

          {/* Gradient Overlay */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent"
            initial={{ opacity: 0 }}
            animate={{ opacity: isHovered ? 1 : 0 }}
            transition={{ duration: 0.3 }}
          />

          {/* Badges */}
          <div className="absolute top-2.5 left-2.5 flex flex-col gap-1.5">
            {discount > 0 && (
              <motion.div
                initial={{ opacity: 0, x: -10, scale: 0.8 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                transition={{ delay: 0.1, ...springs.bouncy }}
              >
                <Badge variant="sale" className="font-bold shadow-lg">
                  -{discount}%
                </Badge>
              </motion.div>
            )}
            {product.is_featured && (
              <motion.div
                initial={{ opacity: 0, x: -10, scale: 0.8 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                transition={{ delay: 0.15, ...springs.bouncy }}
              >
                <Badge variant="gold" className="shadow-lg">
                  <Sparkles className="w-3 h-3 mr-1" />
                  Hit
                </Badge>
              </motion.div>
            )}
          </div>

          {/* Favorite Button */}
          <motion.button
            className="absolute top-2.5 right-2.5 p-2.5 rounded-full bg-white/90 dark:bg-black/50 backdrop-blur-md shadow-lg"
            onClick={handleLike}
            whileTap={{ scale: 0.85 }}
            whileHover={{ scale: 1.1 }}
          >
            <motion.div
              animate={isLiked ? {
                scale: [1, 1.3, 1],
              } : { scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              <Heart
                className={`h-4 w-4 transition-colors duration-200 ${
                  isLiked ? "fill-red-500 text-red-500" : "text-gray-600"
                }`}
              />
            </motion.div>
          </motion.button>

          {/* Action Buttons */}
          <AnimatePresence>
            {product.in_stock && isHovered && (
              <motion.div
                className="absolute bottom-3 left-3 right-3 flex gap-2"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                transition={{ ...springs.snappy }}
              >
                <Button
                  variant="gold"
                  size="sm"
                  className="flex-1 shadow-xl"
                  onClick={handleAddToCart}
                >
                  <ShoppingBag className="h-4 w-4 mr-1.5" />
                  Savatga
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  className="px-3 bg-white/90 backdrop-blur-md shadow-xl"
                  onClick={handleQuickView}
                >
                  <Eye className="h-4 w-4" />
                </Button>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Out of Stock Overlay */}
          {!product.in_stock && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="absolute inset-0 bg-black/40 backdrop-blur-[2px] flex items-center justify-center"
            >
              <Badge variant="secondary" className="text-sm px-4 py-1.5">
                Sotuvda yo'q
              </Badge>
            </motion.div>
          )}
        </div>

        {/* Content */}
        <motion.div
          className="p-3.5"
          animate={{ y: isHovered ? -2 : 0 }}
          transition={{ ...springs.snappy }}
        >
          {/* Category */}
          <p className="text-[11px] text-muted-foreground uppercase tracking-wider mb-1">
            {product.category?.name}
          </p>

          {/* Name */}
          <h3 className="font-medium text-sm leading-tight line-clamp-2 mb-2 group-hover:text-primary transition-colors duration-300">
            {product.name}
          </h3>

          {/* Price */}
          <div className="flex items-baseline gap-2 flex-wrap">
            <motion.span
              className="font-bold text-base gold-text"
              animate={{ scale: isHovered ? 1.02 : 1 }}
              transition={{ ...springs.snappy }}
            >
              {formatPrice(Number(product.price))}
            </motion.span>
            {product.old_price && (
              <span className="text-xs text-muted-foreground line-through">
                {formatPrice(Number(product.old_price))}
              </span>
            )}
          </div>

          {/* Weight */}
          {product.weight && (
            <p className="text-[11px] text-muted-foreground mt-1.5 flex items-center gap-1">
              <span className="w-1 h-1 rounded-full bg-amber-400" />
              {product.weight} gr • {product.metal_type === "gold" ? "Oltin" : product.metal_type === "silver" ? "Kumush" : "Oq oltin"}
            </p>
          )}
        </motion.div>
      </Card>
    </motion.div>
  );
});

// Loading Skeleton with pulse animation
export function ProductCardSkeleton() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-3"
    >
      <Skeleton className="aspect-square rounded-xl" />
      <div className="space-y-2 px-1">
        <Skeleton className="h-3 w-16" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-2/3" />
        <Skeleton className="h-5 w-24" />
      </div>
    </motion.div>
  );
}
