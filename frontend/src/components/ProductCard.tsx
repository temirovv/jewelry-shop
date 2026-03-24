import { memo, useState } from "react";
import { motion } from "framer-motion";
import { Heart, ShoppingBag, Sparkles } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { Skeleton } from "./ui/skeleton";
import { formatPrice } from "../lib/utils";
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
}: ProductCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);

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

  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" } },
      }}
      initial="hidden"
      animate="visible"
      transition={{ delay: index * 0.03 }}
    >
      <Card
        className="overflow-hidden cursor-pointer group border-0 shadow-sm active:scale-[0.98] transition-transform duration-150 bg-card/80"
        onClick={() => onPress?.(product)}
      >
        {/* Image Container */}
        <div className="relative aspect-square overflow-hidden bg-gradient-to-br from-muted/50 to-muted">
          {/* Skeleton while loading */}
          {!imageLoaded && mainImage?.image && (
            <div className="absolute inset-0">
              <Skeleton className="w-full h-full" />
            </div>
          )}

          {/* Product Image */}
          {mainImage?.image ? (
            <img
              src={mainImage.image}
              alt={product.name}
              className={`w-full h-full object-cover transition-all duration-500 ${imageLoaded ? "opacity-100 blur-0 scale-100" : "opacity-0 blur-sm scale-105"}`}
              onLoad={() => setImageLoaded(true)}
              loading="lazy"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900/20 dark:to-amber-800/20">
              <Sparkles className="w-12 h-12 text-amber-400/50" />
            </div>
          )}

          {/* Badges */}
          <div className="absolute top-2.5 left-2.5 flex flex-col gap-1.5">
            {discount > 0 && (
              <Badge variant="sale" className="font-bold shadow-lg">
                -{discount}%
              </Badge>
            )}
            {product.is_featured && (
              <Badge variant="gold" className="shadow-lg">
                <Sparkles className="w-3 h-3 mr-1" />
                Hit
              </Badge>
            )}
          </div>

          {/* Favorite Button */}
          <motion.button
            className="absolute top-2.5 right-2.5 p-2.5 rounded-full bg-white/90 dark:bg-black/50 backdrop-blur-md shadow-lg"
            onClick={handleLike}
            whileTap={{ scale: 0.85 }}
          >
            <motion.div
              animate={isLiked ? { scale: [1, 1.3, 1] } : { scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              <Heart
                className={`h-4 w-4 transition-colors duration-200 ${
                  isLiked ? "fill-red-500 text-red-500" : "text-gray-600"
                }`}
              />
            </motion.div>
          </motion.button>

          {/* Cart Button (mobile) */}
          {product.in_stock && (
            <motion.button
              className="absolute bottom-2.5 right-2.5 w-9 h-9 rounded-full gold-gradient flex items-center justify-center shadow-lg"
              onClick={handleAddToCart}
              whileTap={{ scale: 0.85 }}
            >
              <ShoppingBag className="h-4 w-4 text-white" />
            </motion.button>
          )}

          {/* Out of Stock Overlay */}
          {!product.in_stock && (
            <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px] flex items-center justify-center">
              <Badge variant="secondary" className="text-sm px-4 py-1.5">
                Sotuvda yo'q
              </Badge>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-3.5">
          <p className="text-[11px] text-muted-foreground uppercase tracking-wider mb-1">
            {product.category?.name}
          </p>
          <h3 className="font-medium text-sm leading-tight line-clamp-2 mb-2">
            {product.name}
          </h3>
          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="font-bold text-base gold-text">
              {formatPrice(Number(product.price))}
            </span>
            {product.old_price && (
              <span className="text-xs text-muted-foreground line-through">
                {formatPrice(Number(product.old_price))}
              </span>
            )}
          </div>
          {product.weight && (
            <p className="text-[11px] text-muted-foreground mt-1.5 flex items-center gap-1">
              <span className="w-1 h-1 rounded-full bg-amber-400" />
              {product.weight} gr • {product.metal_type === "gold" ? "Oltin" : product.metal_type === "silver" ? "Kumush" : "Oq oltin"}
            </p>
          )}
        </div>
      </Card>
    </motion.div>
  );
});

// Loading Skeleton
export function ProductCardSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="aspect-square rounded-xl" />
      <div className="space-y-2 px-1">
        <Skeleton className="h-3 w-16" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-2/3" />
        <Skeleton className="h-5 w-24" />
      </div>
    </div>
  );
}
