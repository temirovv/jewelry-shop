import { motion } from "framer-motion";
import { Heart, ShoppingBag } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { formatPrice } from "../lib/utils";
import type { Product } from "../types";

interface ProductCardProps {
  product: Product;
  onPress?: (product: Product) => void;
  onAddToCart?: (product: Product) => void;
}

export function ProductCard({ product, onPress, onAddToCart }: ProductCardProps) {
  const mainImage = product.images.find((img) => img.is_main) || product.images[0];
  const discount = product.old_price
    ? Math.round(((product.old_price - product.price) / product.old_price) * 100)
    : 0;

  return (
    <motion.div
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        className="overflow-hidden cursor-pointer group"
        onClick={() => onPress?.(product)}
      >
        {/* Image Container */}
        <div className="relative aspect-square overflow-hidden bg-muted">
          <img
            src={mainImage?.image || "/placeholder.jpg"}
            alt={product.name}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />

          {/* Badges */}
          <div className="absolute top-2 left-2 flex flex-col gap-1">
            {discount > 0 && (
              <Badge variant="sale">-{discount}%</Badge>
            )}
            {product.is_featured && (
              <Badge variant="gold">Hit</Badge>
            )}
          </div>

          {/* Favorite Button */}
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-2 right-2 bg-white/80 backdrop-blur-sm hover:bg-white"
            onClick={(e) => {
              e.stopPropagation();
              // TODO: Add to favorites
            }}
          >
            <Heart className="h-4 w-4" />
          </Button>

          {/* Quick Add Button */}
          {!product.in_stock ? (
            <div className="absolute bottom-2 left-2 right-2">
              <Badge variant="secondary" className="w-full justify-center py-1">
                Sotuvda yo'q
              </Badge>
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              whileHover={{ opacity: 1, y: 0 }}
              className="absolute bottom-2 left-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <Button
                variant="gold"
                size="sm"
                className="w-full"
                onClick={(e) => {
                  e.stopPropagation();
                  onAddToCart?.(product);
                }}
              >
                <ShoppingBag className="h-4 w-4 mr-2" />
                Savatga
              </Button>
            </motion.div>
          )}
        </div>

        {/* Content */}
        <CardContent className="p-3">
          <p className="text-xs text-muted-foreground mb-1">
            {product.category.name}
          </p>
          <h3 className="font-medium text-sm line-clamp-2 mb-2">
            {product.name}
          </h3>
          <div className="flex items-baseline gap-2">
            <span className="font-bold text-base gold-text">
              {formatPrice(product.price)}
            </span>
            {product.old_price && (
              <span className="text-xs text-muted-foreground line-through">
                {formatPrice(product.old_price)}
              </span>
            )}
          </div>
          {product.weight && (
            <p className="text-xs text-muted-foreground mt-1">
              {product.weight} gr
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
