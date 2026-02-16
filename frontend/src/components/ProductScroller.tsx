import { memo } from "react";
import { motion } from "framer-motion";
import { ShoppingBag, Heart, Sparkles } from "lucide-react";
import { Skeleton } from "./ui/skeleton";
import { Badge } from "./ui/badge";
import { formatPrice } from "../lib/utils";
import { useFavoritesStore } from "../stores/favoritesStore";
import type { Product } from "../types";

interface ProductScrollerProps {
  products: Product[];
  onProductPress: (product: Product) => void;
  onAddToCart: (product: Product) => void;
  loading?: boolean;
}

function CompactCard({
  product,
  index,
  onPress,
  onAddToCart,
}: {
  product: Product;
  index: number;
  onPress: () => void;
  onAddToCart: (e: React.MouseEvent) => void;
}) {
  const { toggleItem, isFavorite } = useFavoritesStore();
  const isLiked = isFavorite(product.id);
  const mainImage = product.images?.find((img) => img.is_main) || product.images?.[0];
  const discount = product.old_price
    ? Math.round(((Number(product.old_price) - Number(product.price)) / Number(product.old_price)) * 100)
    : 0;

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.06, type: "spring", stiffness: 200, damping: 25 }}
      className="shrink-0 w-[165px] cursor-pointer group"
      onClick={onPress}
    >
      {/* Image */}
      <div className="relative aspect-[4/5] rounded-2xl overflow-hidden bg-gradient-to-br from-muted/50 to-muted mb-2.5">
        {mainImage?.image ? (
          <img
            src={mainImage.image}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900/20 dark:to-amber-800/20">
            <Sparkles className="w-10 h-10 text-amber-400/50" />
          </div>
        )}

        {/* Badges */}
        {discount > 0 && (
          <Badge variant="sale" className="absolute top-2 left-2 text-[10px] font-bold shadow-md">
            -{discount}%
          </Badge>
        )}

        {/* Favorite */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggleItem(product);
          }}
          className="absolute top-2 right-2 w-7 h-7 rounded-full bg-white/90 dark:bg-black/50 backdrop-blur-sm flex items-center justify-center shadow-sm"
        >
          <Heart
            className={`w-3.5 h-3.5 ${isLiked ? "fill-red-500 text-red-500" : "text-gray-500"}`}
          />
        </button>

        {/* Cart button */}
        {product.in_stock && (
          <motion.button
            className="absolute bottom-2 right-2 w-8 h-8 rounded-full gold-gradient flex items-center justify-center shadow-lg"
            onClick={onAddToCart}
            whileTap={{ scale: 0.85 }}
          >
            <ShoppingBag className="w-3.5 h-3.5 text-white" />
          </motion.button>
        )}

        {/* Out of stock */}
        {!product.in_stock && (
          <div className="absolute inset-0 bg-black/40 backdrop-blur-[1px] flex items-center justify-center">
            <span className="text-xs text-white font-medium bg-black/50 px-2 py-1 rounded-full">
              Sotuvda yo'q
            </span>
          </div>
        )}
      </div>

      {/* Info */}
      <h3 className="text-sm font-medium leading-tight line-clamp-2 mb-1 px-0.5">
        {product.name}
      </h3>
      <div className="flex items-baseline gap-1.5 px-0.5">
        <span className="font-bold text-sm gold-text">{formatPrice(Number(product.price))}</span>
        {product.old_price && (
          <span className="text-[10px] text-muted-foreground line-through">
            {formatPrice(Number(product.old_price))}
          </span>
        )}
      </div>
    </motion.div>
  );
}

function ScrollerSkeleton() {
  return (
    <div className="flex gap-3 px-4 overflow-hidden">
      {[1, 2, 3].map((i) => (
        <div key={i} className="shrink-0 w-[165px]">
          <Skeleton className="aspect-[4/5] rounded-2xl mb-2.5" />
          <Skeleton className="h-4 w-full mb-1" />
          <Skeleton className="h-4 w-2/3" />
        </div>
      ))}
    </div>
  );
}

export const ProductScroller = memo(function ProductScroller({
  products,
  onProductPress,
  onAddToCart,
  loading = false,
}: ProductScrollerProps) {
  if (loading) return <ScrollerSkeleton />;
  if (products.length === 0) return null;

  return (
    <div className="flex gap-3 px-4 overflow-x-auto scrollbar-hide pb-1">
      {products.map((product, index) => (
        <CompactCard
          key={product.id}
          product={product}
          index={index}
          onPress={() => onProductPress(product)}
          onAddToCart={(e) => {
            e.stopPropagation();
            onAddToCart(product);
          }}
        />
      ))}
    </div>
  );
});
