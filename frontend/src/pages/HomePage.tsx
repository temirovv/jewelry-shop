import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Header } from "../components/Header";
import { HeroBanner } from "../components/HeroBanner";
import { CategorySlider } from "../components/CategorySlider";
import { ProductCard, ProductCardSkeleton } from "../components/ProductCard";
import { CartSheet } from "../components/CartSheet";
import { QuickViewModal } from "../components/QuickViewModal";
import { BottomNav } from "../components/BottomNav";
import { SidebarMenu } from "../components/SidebarMenu";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { getProducts, getCategories } from "../lib/api/products";
import type { Product, Category } from "../types";

export function HomePage() {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState<string>();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCategoriesLoading, setIsCategoriesLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Sidebar Menu
  const [menuOpen, setMenuOpen] = useState(false);

  // Cart
  const [cartOpen, setCartOpen] = useState(false);
  const addItem = useCartStore((state) => state.addItem);

  // Quick View
  const [quickViewProduct, setQuickViewProduct] = useState<Product | null>(null);
  const [quickViewOpen, setQuickViewOpen] = useState(false);

  // Telegram
  const { hapticFeedback } = useTelegram();

  // Fetch Categories
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await getCategories();
        setCategories(data);
      } catch (error) {
        console.error("Categories fetch error:", error);
      } finally {
        setIsCategoriesLoading(false);
      }
    };
    fetchCategories();
  }, []);

  // Fetch Products
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getProducts(
          selectedCategory ? { category: selectedCategory } : undefined
        );
        setProducts(data.results);
      } catch (error) {
        console.error("Products fetch error:", error);
        setError("Mahsulotlarni yuklashda xatolik. Qaytadan urinib ko'ring.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchProducts();
  }, [selectedCategory]);

  const handleAddToCart = useCallback((product: Product, quantity: number = 1) => {
    addItem(product, quantity);
    hapticFeedback?.impactOccurred?.("medium");
    toast.success(`"${product.name}" savatga qo'shildi`);
  }, [addItem, hapticFeedback]);

  const handleQuickView = useCallback((product: Product) => {
    setQuickViewProduct(product);
    setQuickViewOpen(true);
    hapticFeedback?.impactOccurred?.("light");
  }, [hapticFeedback]);

  const handleProductPress = useCallback((product: Product) => {
    hapticFeedback?.impactOccurred?.("light");
    navigate(`/product/${product.id}`);
  }, [hapticFeedback, navigate]);

  const handleTabChange = useCallback((tab: "home" | "search" | "favorites" | "cart" | "profile") => {
    hapticFeedback?.impactOccurred?.("light");
    if (tab === "cart") {
      setCartOpen(true);
    } else if (tab === "search") {
      navigate("/search");
    } else if (tab === "favorites") {
      navigate("/favorites");
    } else if (tab === "profile") {
      navigate("/profile");
    }
  }, [hapticFeedback, navigate]);

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <Header
        onMenuClick={() => setMenuOpen(true)}
        onCartClick={() => setCartOpen(true)}
        onSearchClick={() => navigate("/search")}
      />

      {/* Hero Banner */}
      <div className="pt-2 pb-1">
        <HeroBanner />
      </div>

      {/* Categories */}
      <CategorySlider
        categories={categories}
        selectedCategory={selectedCategory}
        onSelect={setSelectedCategory}
        loading={isCategoriesLoading}
      />

      {/* Section Title */}
      <div className="flex items-center justify-between px-4 py-3">
        <motion.h3
          key={selectedCategory || "all"}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="font-semibold text-lg"
        >
          {selectedCategory
            ? categories.find((c) => c.slug === selectedCategory)?.name || "Mahsulotlar"
            : "Barcha mahsulotlar"}
        </motion.h3>
        <span className="text-sm text-muted-foreground">
          {isLoading ? "..." : `${products.length} ta`}
        </span>
      </div>

      {/* Products Grid */}
      <div className="px-4">
        <AnimatePresence mode="wait">
          {isLoading ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="grid grid-cols-2 gap-3"
            >
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <ProductCardSkeleton key={i} />
              ))}
            </motion.div>
          ) : error ? (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-16"
            >
              <div className="text-5xl mb-4">😕</div>
              <h3 className="font-medium mb-1 text-destructive">Xatolik</h3>
              <p className="text-sm text-muted-foreground mb-4">{error}</p>
              <button
                onClick={() => setSelectedCategory(selectedCategory)}
                className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium"
              >
                Qayta yuklash
              </button>
            </motion.div>
          ) : products.length === 0 ? (
            <motion.div
              key="empty"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-16"
            >
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="font-medium mb-1">Mahsulot topilmadi</h3>
              <p className="text-sm text-muted-foreground">
                Boshqa kategoriyani tanlang
              </p>
            </motion.div>
          ) : (
            <motion.div
              key="products"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="grid grid-cols-2 gap-3"
            >
              {products.map((product, index) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  index={index}
                  onPress={handleProductPress}
                  onAddToCart={handleAddToCart}
                  onQuickView={handleQuickView}
                />
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Bottom Navigation */}
      <BottomNav activeTab="home" onTabChange={handleTabChange} />

      {/* Cart Sheet */}
      <CartSheet
        open={cartOpen}
        onOpenChange={setCartOpen}
        onCheckout={() => {
          setCartOpen(false);
          navigate("/checkout");
        }}
      />

      {/* Quick View Modal */}
      <QuickViewModal
        product={quickViewProduct}
        open={quickViewOpen}
        onOpenChange={setQuickViewOpen}
        onAddToCart={handleAddToCart}
        onViewDetail={(product) => {
          setQuickViewOpen(false);
          navigate(`/product/${product.id}`);
        }}
      />

      {/* Sidebar Menu */}
      <SidebarMenu open={menuOpen} onOpenChange={setMenuOpen} />
    </div>
  );
}
