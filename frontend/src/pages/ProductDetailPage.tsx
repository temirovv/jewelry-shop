import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  Heart,
  ShoppingBag,
  Share2,
  ChevronLeft,
  ChevronRight,
  Minus,
  Plus,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Skeleton } from "../components/ui/skeleton";
import { useCartStore } from "../stores/cartStore";
import { useFavoritesStore } from "../stores/favoritesStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { getProduct } from "../lib/api/products";
import { formatPrice } from "../lib/utils";
import type { Product } from "../types";

export function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [quantity, setQuantity] = useState(1);

  const addItem = useCartStore((state) => state.addItem);
  const { toggleItem, isFavorite } = useFavoritesStore();
  const { hapticFeedback, showBackButton, hideBackButton } = useTelegram();

  const isInFavorites = product ? isFavorite(product.id) : false;

  useEffect(() => {
    showBackButton(() => navigate(-1));
    return () => hideBackButton();
  }, [showBackButton, hideBackButton, navigate]);

  useEffect(() => {
    const fetchProduct = async () => {
      if (!id) return;
      setIsLoading(true);
      setError(null);
      try {
        const data = await getProduct(Number(id));
        setProduct(data);
      } catch (err) {
        setError("Mahsulot topilmadi");
      } finally {
        setIsLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  const handleAddToCart = () => {
    if (!product) return;
    addItem(product, quantity);
    hapticFeedback?.impactOccurred?.("medium");
    toast.success(`"${product.name}" savatga qo'shildi`);
  };

  const handleToggleFavorite = () => {
    if (!product) return;
    toggleItem(product);
    hapticFeedback?.impactOccurred?.("light");
    toast.success(
      isInFavorites ? "Sevimlilardan o'chirildi" : "Sevimlilarga qo'shildi"
    );
  };

  const handleShare = async () => {
    if (!product) return;
    hapticFeedback?.impactOccurred?.("light");
    try {
      await navigator.share({
        title: product.name,
        text: `${product.name} - ${formatPrice(product.price)}`,
        url: window.location.href,
      });
    } catch {
      toast.info("Ulashish imkonsiz");
    }
  };

  const nextImage = () => {
    if (!product) return;
    setCurrentImageIndex((prev) =>
      prev === product.images.length - 1 ? 0 : prev + 1
    );
    hapticFeedback?.selectionChanged?.();
  };

  const prevImage = () => {
    if (!product) return;
    setCurrentImageIndex((prev) =>
      prev === 0 ? product.images.length - 1 : prev - 1
    );
    hapticFeedback?.selectionChanged?.();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <div className="aspect-square">
          <Skeleton className="w-full h-full" />
        </div>
        <div className="p-4 space-y-4">
          <Skeleton className="h-8 w-3/4" />
          <Skeleton className="h-6 w-1/2" />
          <Skeleton className="h-24 w-full" />
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
        <div className="text-6xl mb-4">😕</div>
        <h2 className="text-xl font-semibold mb-2">Mahsulot topilmadi</h2>
        <p className="text-muted-foreground mb-4 text-center">{error}</p>
        <Button onClick={() => navigate(-1)}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Orqaga qaytish
        </Button>
      </div>
    );
  }

  const discountPercent = product.old_price
    ? Math.round(((product.old_price - product.price) / product.old_price) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-background pb-32">
      {/* Image Gallery */}
      <div className="relative aspect-square bg-muted">
        {/* Back button */}
        <button
          onClick={() => navigate(-1)}
          className="absolute top-4 left-4 z-10 w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm flex items-center justify-center shadow-lg"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>

        {/* Action buttons */}
        <div className="absolute top-4 right-4 z-10 flex gap-2">
          <button
            onClick={handleToggleFavorite}
            className="w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm flex items-center justify-center shadow-lg"
          >
            <Heart
              className={`w-5 h-5 ${
                isInFavorites ? "fill-red-500 text-red-500" : ""
              }`}
            />
          </button>
          <button
            onClick={handleShare}
            className="w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm flex items-center justify-center shadow-lg"
          >
            <Share2 className="w-5 h-5" />
          </button>
        </div>

        {/* Main Image */}
        <AnimatePresence mode="wait">
          <motion.img
            key={currentImageIndex}
            src={product.images[currentImageIndex]?.image || "/placeholder.jpg"}
            alt={product.name}
            className="w-full h-full object-cover"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          />
        </AnimatePresence>

        {/* Navigation arrows */}
        {product.images.length > 1 && (
          <>
            <button
              onClick={prevImage}
              className="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-background/60 backdrop-blur-sm flex items-center justify-center"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            <button
              onClick={nextImage}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-background/60 backdrop-blur-sm flex items-center justify-center"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          </>
        )}

        {/* Image indicators */}
        {product.images.length > 1 && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5">
            {product.images.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentImageIndex(index)}
                className={`w-2 h-2 rounded-full transition-all ${
                  index === currentImageIndex
                    ? "w-6 bg-primary"
                    : "bg-background/60"
                }`}
              />
            ))}
          </div>
        )}

        {/* Discount badge */}
        {discountPercent > 0 && (
          <Badge className="absolute top-4 left-16 bg-red-500 text-white">
            -{discountPercent}%
          </Badge>
        )}
      </div>

      {/* Product Info */}
      <div className="p-4 space-y-4">
        {/* Category */}
        <Badge variant="secondary">{product.category.name}</Badge>

        {/* Name */}
        <h1 className="text-2xl font-bold">{product.name}</h1>

        {/* Price */}
        <div className="flex items-baseline gap-3">
          <span className="text-2xl font-bold text-primary">
            {formatPrice(product.price)}
          </span>
          {product.old_price && (
            <span className="text-lg text-muted-foreground line-through">
              {formatPrice(product.old_price)}
            </span>
          )}
        </div>

        {/* Specs */}
        <div className="grid grid-cols-2 gap-3">
          <div className="p-3 rounded-xl bg-muted/50">
            <span className="text-sm text-muted-foreground">Metall turi</span>
            <p className="font-medium capitalize">
              {product.metal_type.replace("_", " ")}
            </p>
          </div>
          <div className="p-3 rounded-xl bg-muted/50">
            <span className="text-sm text-muted-foreground">Og'irligi</span>
            <p className="font-medium">{product.weight} gr</p>
          </div>
          {product.size && (
            <div className="p-3 rounded-xl bg-muted/50">
              <span className="text-sm text-muted-foreground">O'lchami</span>
              <p className="font-medium">{product.size}</p>
            </div>
          )}
          <div className="p-3 rounded-xl bg-muted/50">
            <span className="text-sm text-muted-foreground">Mavjudligi</span>
            <p
              className={`font-medium ${
                product.in_stock ? "text-green-600" : "text-red-500"
              }`}
            >
              {product.in_stock ? "Bor" : "Yo'q"}
            </p>
          </div>
        </div>

        {/* Description */}
        <div>
          <h3 className="font-semibold mb-2">Tavsif</h3>
          <p className="text-muted-foreground leading-relaxed">
            {product.description}
          </p>
        </div>
      </div>

      {/* Bottom Action Bar */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-background/80 backdrop-blur-xl border-t border-border/50 safe-area-bottom">
        <div className="flex items-center gap-4">
          {/* Quantity Selector */}
          <div className="flex items-center gap-2 bg-muted rounded-xl p-1">
            <button
              onClick={() => setQuantity((q) => Math.max(1, q - 1))}
              className="w-10 h-10 rounded-lg flex items-center justify-center hover:bg-background transition-colors"
              disabled={quantity <= 1}
            >
              <Minus className="w-4 h-4" />
            </button>
            <span className="w-8 text-center font-medium">{quantity}</span>
            <button
              onClick={() => setQuantity((q) => q + 1)}
              className="w-10 h-10 rounded-lg flex items-center justify-center hover:bg-background transition-colors"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>

          {/* Add to Cart Button */}
          <Button
            className="flex-1 h-12 gold-gradient text-white font-medium rounded-xl"
            onClick={handleAddToCart}
            disabled={!product.in_stock}
          >
            <ShoppingBag className="w-5 h-5 mr-2" />
            {product.in_stock ? "Savatga qo'shish" : "Mavjud emas"}
          </Button>
        </div>
      </div>
    </div>
  );
}
