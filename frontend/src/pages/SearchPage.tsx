import { useState, useEffect, useCallback, useMemo } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  X,
  SlidersHorizontal,
  ArrowUpDown,
} from "lucide-react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { ProductCard, ProductCardSkeleton } from "../components/ProductCard";
import { BottomNav } from "../components/BottomNav";
import { CartSheet } from "../components/CartSheet";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { getProducts, getCategories, type ProductFilters } from "../lib/api/products";
import type { Product, Category } from "../types";

const SORT_OPTIONS = [
  { value: "", label: "Standart" },
  { value: "-created_at", label: "Yangi" },
  { value: "price", label: "Arzon" },
  { value: "-price", label: "Qimmat" },
];

const METAL_TYPES = [
  { value: "", label: "Barchasi" },
  { value: "gold", label: "Oltin" },
  { value: "silver", label: "Kumush" },
  { value: "platinum", label: "Platina" },
  { value: "white_gold", label: "Oq oltin" },
];

export function SearchPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState(
    searchParams.get("category") || ""
  );
  const [selectedMetal, setSelectedMetal] = useState(
    searchParams.get("metal_type") || ""
  );
  const [sortBy, setSortBy] = useState(searchParams.get("ordering") || "");

  const { hapticFeedback } = useTelegram();
  const addItem = useCartStore((state) => state.addItem);

  // Fetch categories
  useEffect(() => {
    getCategories().then(setCategories).catch(console.error);
  }, []);

  // Search products
  const searchProducts = useCallback(async () => {
    setIsLoading(true);
    try {
      const filters: ProductFilters = {};
      if (query.trim()) filters.search = query.trim();
      if (selectedCategory) filters.category = selectedCategory;
      if (selectedMetal) filters.metal_type = selectedMetal;
      if (sortBy) filters.ordering = sortBy;

      const data = await getProducts(filters);
      setProducts(data.results);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [query, selectedCategory, selectedMetal, sortBy]);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(searchProducts, 300);
    return () => clearTimeout(timer);
  }, [searchProducts]);

  // Update URL params
  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (selectedCategory) params.set("category", selectedCategory);
    if (selectedMetal) params.set("metal_type", selectedMetal);
    if (sortBy) params.set("ordering", sortBy);
    setSearchParams(params, { replace: true });
  }, [query, selectedCategory, selectedMetal, sortBy, setSearchParams]);

  const handleAddToCart = useCallback(
    (product: Product, quantity: number = 1) => {
      addItem(product, quantity);
      hapticFeedback?.impactOccurred?.("medium");
      toast.success(`"${product.name}" savatga qo'shildi`);
    },
    [addItem, hapticFeedback]
  );

  const handleProductPress = useCallback(
    (product: Product) => {
      hapticFeedback?.impactOccurred?.("light");
      navigate(`/product/${product.id}`);
    },
    [hapticFeedback, navigate]
  );

  const clearFilters = () => {
    setSelectedCategory("");
    setSelectedMetal("");
    setSortBy("");
    hapticFeedback?.impactOccurred?.("light");
  };

  const hasFilters = selectedCategory || selectedMetal || sortBy;

  const activeFiltersCount = useMemo(() => {
    let count = 0;
    if (selectedCategory) count++;
    if (selectedMetal) count++;
    if (sortBy) count++;
    return count;
  }, [selectedCategory, selectedMetal, sortBy]);

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Search Header */}
      <div className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50 px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              placeholder="Qidirish..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="pl-10 pr-10 h-11"
              autoFocus
            />
            {query && (
              <button
                onClick={() => setQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground hover:text-foreground"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
          <Button
            variant="outline"
            size="icon"
            className="relative h-11 w-11 shrink-0"
            onClick={() => setShowFilters(!showFilters)}
          >
            <SlidersHorizontal className="w-5 h-5" />
            {activeFiltersCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full gold-gradient text-[10px] font-bold text-white flex items-center justify-center">
                {activeFiltersCount}
              </span>
            )}
          </Button>
        </div>

        {/* Filters Panel */}
        <AnimatePresence>
          {showFilters && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden"
            >
              <div className="pt-4 space-y-4">
                {/* Categories */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Kategoriya
                  </label>
                  <div className="flex flex-wrap gap-2">
                    <Badge
                      variant={!selectedCategory ? "default" : "outline"}
                      className="cursor-pointer"
                      onClick={() => setSelectedCategory("")}
                    >
                      Barchasi
                    </Badge>
                    {categories.map((cat) => (
                      <Badge
                        key={cat.id}
                        variant={
                          selectedCategory === cat.slug ? "default" : "outline"
                        }
                        className="cursor-pointer"
                        onClick={() => setSelectedCategory(cat.slug)}
                      >
                        {cat.name}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Metal Type */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Metall turi
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {METAL_TYPES.map((metal) => (
                      <Badge
                        key={metal.value}
                        variant={
                          selectedMetal === metal.value ? "default" : "outline"
                        }
                        className="cursor-pointer"
                        onClick={() => setSelectedMetal(metal.value)}
                      >
                        {metal.label}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Sort */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Saralash
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {SORT_OPTIONS.map((option) => (
                      <Badge
                        key={option.value}
                        variant={sortBy === option.value ? "default" : "outline"}
                        className="cursor-pointer"
                        onClick={() => setSortBy(option.value)}
                      >
                        <ArrowUpDown className="w-3 h-3 mr-1" />
                        {option.label}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Clear Filters */}
                {hasFilters && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={clearFilters}
                    className="text-muted-foreground"
                  >
                    <X className="w-4 h-4 mr-1" />
                    Filtrlarni tozalash
                  </Button>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Results */}
      <div className="px-4 py-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold">
            {query ? `"${query}" uchun natijalar` : "Barcha mahsulotlar"}
          </h2>
          <span className="text-sm text-muted-foreground">
            {isLoading ? "..." : `${products.length} ta`}
          </span>
        </div>

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
                <Search className="w-10 h-10 text-muted-foreground" />
              </motion.div>
              <h3 className="font-medium mb-1">Hech narsa topilmadi</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Boshqa so'z yoki filtr bilan urinib ko'ring
              </p>
              {hasFilters && (
                <Button variant="outline" onClick={clearFilters}>
                  Filtrlarni tozalash
                </Button>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="products"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="grid grid-cols-2 gap-3"
            >
              {products.map((product, index) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  index={index}
                  onPress={handleProductPress}
                  onAddToCart={handleAddToCart}
                  onQuickView={handleProductPress}
                />
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Bottom Navigation */}
      <BottomNav
        activeTab="search"
        onTabChange={(tab) => {
          if (tab === "cart") setCartOpen(true);
          else if (tab === "home") navigate("/");
          else if (tab === "favorites") navigate("/favorites");
          else if (tab === "profile") navigate("/profile");
        }}
      />

      {/* Cart Sheet */}
      <CartSheet
        open={cartOpen}
        onOpenChange={setCartOpen}
        onCheckout={() => {
          setCartOpen(false);
          navigate("/checkout");
        }}
      />
    </div>
  );
}
