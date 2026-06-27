import { useState, useEffect, useCallback, useMemo } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  X,
  SlidersHorizontal,
  ArrowUpDown,
  Loader2,
} from "lucide-react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { ProductCard, ProductCardSkeleton } from "../components/ProductCard";
import { BottomNav } from "../components/BottomNav";
import { CartSheet } from "../components/CartSheet";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../stores/toastStore";
import { getProducts, getProductsByUrl, getCategories, type ProductFilters } from "../lib/api/products";
import { getBrands } from "../lib/api/brands";
import type { Product, Category, Brand } from "../types";

const SORT_OPTIONS = [
  { value: "", label: "Standart" },
  { value: "-created_at", label: "Yangi" },
  { value: "price", label: "Arzon" },
  { value: "-price", label: "Qimmat" },
];

const PRODUCT_TYPES = [
  { value: "", label: "Barchasi" },
  { value: "skincare", label: "Teri parvarishi" },
  { value: "makeup", label: "Makiyaj" },
  { value: "perfume", label: "Parfyumeriya" },
  { value: "haircare", label: "Soch parvarishi" },
  { value: "bodycare", label: "Tana parvarishi" },
];

export function SearchPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState(
    searchParams.get("category") || ""
  );
  const [selectedBrand, setSelectedBrand] = useState(
    searchParams.get("brand") || ""
  );
  const [selectedType, setSelectedType] = useState(
    searchParams.get("product_type") || ""
  );
  const [sortBy, setSortBy] = useState(searchParams.get("ordering") || "");
  const [minPrice, setMinPrice] = useState(searchParams.get("min_price") || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("max_price") || "");

  const { hapticFeedback } = useTelegram();
  const addItem = useCartStore((state) => state.addItem);

  // Fetch categories & brands
  useEffect(() => {
    getCategories().then(setCategories).catch(() => {
      toast.error("Kategoriyalarni yuklashda xatolik");
    });
    getBrands().then(setBrands).catch(() => {
      toast.error("Brendlarni yuklashda xatolik");
    });
  }, []);

  // Search products
  const searchProducts = useCallback(async () => {
    setIsLoading(true);
    setNextPage(null);
    try {
      const filters: ProductFilters = {};
      if (query.trim()) filters.search = query.trim();
      if (selectedCategory) filters.category = selectedCategory;
      if (selectedBrand) filters.brand = selectedBrand;
      if (selectedType) filters.product_type = selectedType;
      if (sortBy) filters.ordering = sortBy;
      if (minPrice) filters.min_price = Number(minPrice);
      if (maxPrice) filters.max_price = Number(maxPrice);

      const data = await getProducts(filters);
      setProducts(data.results);
      setNextPage(data.next);
    } catch {
      toast.error("Qidiruv natijalarini yuklashda xatolik");
    } finally {
      setIsLoading(false);
    }
  }, [query, selectedCategory, selectedBrand, selectedType, sortBy, minPrice, maxPrice]);

  const loadMoreProducts = useCallback(async () => {
    if (!nextPage || isLoadingMore) return;
    setIsLoadingMore(true);
    try {
      const data = await getProductsByUrl(nextPage);
      setProducts((prev) => [...prev, ...data.results]);
      setNextPage(data.next);
    } catch {
      toast.error("Mahsulotlarni yuklashda xatolik");
    } finally {
      setIsLoadingMore(false);
    }
  }, [nextPage, isLoadingMore]);

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
    if (selectedBrand) params.set("brand", selectedBrand);
    if (selectedType) params.set("product_type", selectedType);
    if (sortBy) params.set("ordering", sortBy);
    if (minPrice) params.set("min_price", minPrice);
    if (maxPrice) params.set("max_price", maxPrice);
    setSearchParams(params, { replace: true });
  }, [query, selectedCategory, selectedBrand, selectedType, sortBy, minPrice, maxPrice, setSearchParams]);

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
    setSelectedBrand("");
    setSelectedType("");
    setSortBy("");
    setMinPrice("");
    setMaxPrice("");
    hapticFeedback?.impactOccurred?.("light");
  };

  const hasFilters = selectedCategory || selectedBrand || selectedType || sortBy || minPrice || maxPrice;

  const activeFiltersCount = useMemo(() => {
    let count = 0;
    if (selectedCategory) count++;
    if (selectedBrand) count++;
    if (selectedType) count++;
    if (sortBy) count++;
    if (minPrice || maxPrice) count++;
    return count;
  }, [selectedCategory, selectedBrand, selectedType, sortBy, minPrice, maxPrice]);

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

                {/* Product Type */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Mahsulot turi
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {PRODUCT_TYPES.map((type) => (
                      <Badge
                        key={type.value}
                        variant={
                          selectedType === type.value ? "default" : "outline"
                        }
                        className="cursor-pointer"
                        onClick={() => setSelectedType(type.value)}
                      >
                        {type.label}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Brand */}
                {brands.length > 0 && (
                  <div>
                    <label className="text-sm font-medium mb-2 block">
                      Brend
                    </label>
                    <div className="flex flex-wrap gap-2">
                      <Badge
                        variant={!selectedBrand ? "default" : "outline"}
                        className="cursor-pointer"
                        onClick={() => setSelectedBrand("")}
                      >
                        Barchasi
                      </Badge>
                      {brands.map((brand) => (
                        <Badge
                          key={brand.id}
                          variant={
                            selectedBrand === brand.slug ? "default" : "outline"
                          }
                          className="cursor-pointer"
                          onClick={() => setSelectedBrand(brand.slug)}
                        >
                          {brand.name}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Price Range */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Narx oralig'i
                  </label>
                  <div className="flex items-center gap-2">
                    <Input
                      type="number"
                      placeholder="dan"
                      value={minPrice}
                      onChange={(e) => setMinPrice(e.target.value)}
                      className="h-9 text-sm"
                      min={0}
                    />
                    <span className="text-muted-foreground text-sm shrink-0">—</span>
                    <Input
                      type="number"
                      placeholder="gacha"
                      value={maxPrice}
                      onChange={(e) => setMaxPrice(e.target.value)}
                      className="h-9 text-sm"
                      min={0}
                    />
                    <span className="text-muted-foreground text-xs shrink-0">so'm</span>
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
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-50px" }}
              transition={{ staggerChildren: 0.06 }}
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

        {/* Ko'proq ko'rsatish */}
        {nextPage && !isLoading && (
          <div className="flex justify-center mt-6">
            <Button
              variant="outline"
              onClick={loadMoreProducts}
              disabled={isLoadingMore}
              className="px-8"
            >
              {isLoadingMore ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : null}
              {isLoadingMore ? "Yuklanmoqda..." : "Ko'proq ko'rsatish"}
            </Button>
          </div>
        )}
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
