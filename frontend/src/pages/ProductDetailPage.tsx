import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  Heart,
  ShoppingBag,
  Share2,
  Minus,
  Plus,
  PackageX,
  Scale,
  Gem,
  Ruler,
  CircleCheck,
  CircleX,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Skeleton } from "../components/ui/skeleton";
import { SectionHeader } from "../components/SectionHeader";
import { ProductScroller } from "../components/ProductScroller";
import { useCartStore } from "../stores/cartStore";
import { useFavoritesStore } from "../stores/favoritesStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { getProduct, getProducts } from "../lib/api/products";
import { formatPrice } from "../lib/utils";
import { staggerContainerVariants, staggerItemVariants } from "../lib/animations";
import type { Product } from "../types";

export function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [isZoomed, setIsZoomed] = useState(false);
  const [relatedProducts, setRelatedProducts] = useState<Product[]>([]);

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

  // Fetch related products
  useEffect(() => {
    if (product?.category?.slug) {
      getProducts({ category: product.category.slug })
        .then((data) => {
          setRelatedProducts(
            data.results.filter((p) => p.id !== product.id).slice(0, 8)
          );
        })
        .catch(() => {});
    }
  }, [product?.category?.slug, product?.id]);

  // Reset zoom on image change
  useEffect(() => {
    setIsZoomed(false);
  }, [currentImageIndex]);

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
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", damping: 15 }}
          className="w-24 h-24 rounded-full bg-muted flex items-center justify-center mb-5"
        >
          <PackageX className="w-12 h-12 text-muted-foreground" />
        </motion.div>
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

  const metalLabels: Record<string, string> = {
    gold: "Oltin",
    silver: "Kumush",
    platinum: "Platina",
    white_gold: "Oq oltin",
  };

  const specs = [
    { icon: Gem, label: "Metall turi", value: metalLabels[product.metal_type] || product.metal_type },
    { icon: Scale, label: "Og'irligi", value: `${product.weight} gr` },
    ...(product.size ? [{ icon: Ruler, label: "O'lchami", value: product.size }] : []),
    {
      icon: product.in_stock ? CircleCheck : CircleX,
      label: "Mavjudligi",
      value: product.in_stock ? "Bor" : "Yo'q",
      color: product.in_stock ? "text-green-600" : "text-red-500",
    },
  ];

  return (
    <div className="min-h-screen bg-background pb-32">
      {/* Image Gallery */}
      <div className="relative aspect-square bg-muted overflow-hidden">
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

        {/* Main Image with swipe & zoom */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentImageIndex}
            drag={!isZoomed ? "x" : false}
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.15}
            onDragEnd={(_, info) => {
              if (info.offset.x > 50) prevImage();
              else if (info.offset.x < -50) nextImage();
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="w-full h-full cursor-grab active:cursor-grabbing"
          >
            <motion.img
              src={product.images[currentImageIndex]?.image || "/placeholder.jpg"}
              alt={product.name}
              className="w-full h-full object-cover select-none"
              animate={{ scale: isZoomed ? 2 : 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              onDoubleClick={() => setIsZoomed(!isZoomed)}
              style={{
                cursor: isZoomed ? "zoom-out" : "zoom-in",
                transformOrigin: "center center",
              }}
              draggable={false}
            />
          </motion.div>
        </AnimatePresence>

        {/* Image counter */}
        {product.images.length > 1 && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-2.5 py-1 rounded-full bg-black/40 backdrop-blur-sm text-white text-xs font-medium">
            {currentImageIndex + 1} / {product.images.length}
          </div>
        )}

        {/* Image indicators — premium style */}
        {product.images.length > 1 && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5">
            {product.images.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentImageIndex(index)}
                className={`h-2.5 rounded-full transition-all duration-300 ${
                  index === currentImageIndex
                    ? "w-8 gold-gradient shadow-md"
                    : "w-2.5 bg-white/60 backdrop-blur-sm"
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
      <div className="p-4 space-y-5">
        {/* Category */}
        <Badge variant="secondary">{product.category.name}</Badge>

        {/* Name */}
        <h1 className="text-2xl font-display font-bold">{product.name}</h1>

        {/* Price */}
        <div className="flex items-baseline gap-3">
          <span className="text-2xl font-display font-bold text-primary">
            {formatPrice(product.price)}
          </span>
          {product.old_price && (
            <span className="text-lg text-muted-foreground line-through">
              {formatPrice(product.old_price)}
            </span>
          )}
          {discountPercent > 0 && (
            <Badge variant="sale" className="text-xs">-{discountPercent}%</Badge>
          )}
        </div>

        {/* Specs — premium cards with icons */}
        <motion.div
          variants={staggerContainerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-2 gap-3"
        >
          {specs.map((spec, i) => (
            <motion.div
              key={i}
              variants={staggerItemVariants}
              className="p-3.5 rounded-2xl bg-gradient-to-br from-amber-50/50 to-transparent dark:from-amber-900/10 dark:to-transparent border border-amber-100/50 dark:border-amber-900/20"
            >
              <spec.icon className="w-5 h-5 text-primary mb-2" />
              <span className="text-xs text-muted-foreground block">{spec.label}</span>
              <p className={`font-semibold text-sm ${spec.color || ""}`}>
                {spec.value}
              </p>
            </motion.div>
          ))}
        </motion.div>

        {/* Description */}
        <div>
          <h3 className="font-display font-semibold mb-2">Tavsif</h3>
          <p className="text-muted-foreground leading-relaxed text-sm">
            {product.description}
          </p>
        </div>
      </div>

      {/* Related Products */}
      {relatedProducts.length > 0 && (
        <div className="mt-2 pb-4">
          <SectionHeader
            title="O'xshash mahsulotlar"
            onAction={() => navigate(`/search?category=${product.category.slug}`)}
          />
          <ProductScroller
            products={relatedProducts}
            onProductPress={(p) => {
              navigate(`/product/${p.id}`);
              window.scrollTo(0, 0);
            }}
            onAddToCart={(p) => {
              addItem(p, 1);
              hapticFeedback?.impactOccurred?.("medium");
              toast.success(`"${p.name}" savatga qo'shildi`);
            }}
          />
        </div>
      )}

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
