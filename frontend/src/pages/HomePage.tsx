import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { AlertCircle, Search as SearchIcon } from "lucide-react";
import { Header } from "../components/Header";
import { HeroBanner } from "../components/HeroBanner";
import { CategorySlider } from "../components/CategorySlider";
import { SectionHeader } from "../components/SectionHeader";
import { ProductScroller } from "../components/ProductScroller";
import { ProductCard, ProductCardSkeleton } from "../components/ProductCard";
import { CartSheet } from "../components/CartSheet";
import { QuickViewModal } from "../components/QuickViewModal";
import { BottomNav } from "../components/BottomNav";
import { SidebarMenu } from "../components/SidebarMenu";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { getProducts, getCategories, getNewArrivals, getFeaturedProducts } from "../lib/api/products";
import { scrollRevealVariants } from "../lib/animations";
import type { Product, Category } from "../types";

export function HomePage() {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState<string>();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCategoriesLoading, setIsCategoriesLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // New sections
  const [newArrivals, setNewArrivals] = useState<Product[]>([]);
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [isNewArrivalsLoading, setIsNewArrivalsLoading] = useState(true);
  const [isFeaturedLoading, setIsFeaturedLoading] = useState(true);

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

  // Fetch New Arrivals & Featured (parallel)
  useEffect(() => {
    getNewArrivals()
      .then(setNewArrivals)
      .catch(() => {})
      .finally(() => setIsNewArrivalsLoading(false));

    getFeaturedProducts()
      .then(setFeaturedProducts)
      .catch(() => {})
      .finally(() => setIsFeaturedLoading(false));
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
        <HeroBanner onExplore={() => navigate("/search")} />
      </div>

      {/* Categories */}
      <CategorySlider
        categories={categories}
        selectedCategory={selectedCategory}
        onSelect={setSelectedCategory}
        loading={isCategoriesLoading}
      />

      {/* New Arrivals Section */}
      <motion.div
        variants={scrollRevealVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-50px" }}
      >
        <SectionHeader
          title="Yangi kelganlar"
          subtitle="Eng so'nggi mahsulotlar"
          onAction={() => navigate("/search?ordering=-created_at")}
        />
        <ProductScroller
          products={newArrivals}
          onProductPress={handleProductPress}
          onAddToCart={handleAddToCart}
          loading={isNewArrivalsLoading}
        />
      </motion.div>

      {/* Featured Section */}
      <motion.div
        variants={scrollRevealVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-50px" }}
      >
        <SectionHeader
          title="Mashhur"
          subtitle="Eng ko'p sotilganlar"
          onAction={() => navigate("/search?is_featured=true")}
        />
        <ProductScroller
          products={featuredProducts}
          onProductPress={handleProductPress}
          onAddToCart={handleAddToCart}
          loading={isFeaturedLoading}
        />
      </motion.div>

      {/* All Products Section */}
      <motion.div
        variants={scrollRevealVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-50px" }}
      >
        <div className="flex items-center justify-between px-4 pt-6 pb-3">
          <div>
            <motion.h2
              key={selectedCategory || "all"}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-lg font-display font-bold tracking-tight"
            >
              {selectedCategory
                ? categories.find((c) => c.slug === selectedCategory)?.name || "Mahsulotlar"
                : "Barcha mahsulotlar"}
            </motion.h2>
          </div>
          <span className="text-sm text-muted-foreground">
            {isLoading ? "..." : `${products.length} ta`}
          </span>
        </div>
      </motion.div>

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
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", damping: 15, delay: 0.1 }}
                className="w-20 h-20 rounded-full bg-destructive/10 flex items-center justify-center mx-auto mb-5"
              >
                <AlertCircle className="w-10 h-10 text-destructive" />
              </motion.div>
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
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", damping: 15, delay: 0.1 }}
                className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mx-auto mb-5"
              >
                <SearchIcon className="w-10 h-10 text-muted-foreground" />
              </motion.div>
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
