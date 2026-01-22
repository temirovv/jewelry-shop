import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Header } from "../components/Header";
import { CategorySlider } from "../components/CategorySlider";
import { ProductCard } from "../components/ProductCard";
import { Skeleton } from "../components/ui/skeleton";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import type { Product, Category } from "../types";

// Mock data - keyinchalik API dan olinadi
const MOCK_CATEGORIES: Category[] = [
  { id: 1, name: "Uzuklar", slug: "rings", icon: "💍" },
  { id: 2, name: "Sirg'alar", slug: "earrings", icon: "✨" },
  { id: 3, name: "Marjonlar", slug: "necklaces", icon: "📿" },
  { id: 4, name: "Bilaguzuklar", slug: "bracelets", icon: "⌚" },
  { id: 5, name: "To'plamlar", slug: "sets", icon: "🎁" },
];

const MOCK_PRODUCTS: Product[] = [
  {
    id: 1,
    name: "Oltin uzuk 585 proba, brilliant bilan",
    description: "Klassik dizayn, 585 proba oltin",
    price: 2500000,
    old_price: 3000000,
    images: [{ id: 1, image: "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400", is_main: true }],
    category: { id: 1, name: "Uzuklar", slug: "rings" },
    metal_type: "gold",
    weight: 3.5,
    size: "17",
    in_stock: true,
    is_featured: true,
    created_at: "2024-01-01",
  },
  {
    id: 2,
    name: "Sirg'a to'plami, marvarid bilan",
    description: "Tabiiy marvarid, 585 proba oltin",
    price: 1800000,
    images: [{ id: 2, image: "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400", is_main: true }],
    category: { id: 2, name: "Sirg'alar", slug: "earrings" },
    metal_type: "gold",
    weight: 2.8,
    in_stock: true,
    is_featured: false,
    created_at: "2024-01-02",
  },
  {
    id: 3,
    name: "Marjon zanjir, italyan to'qish",
    description: "585 proba oltin, italyan ishlab chiqarish",
    price: 4200000,
    old_price: 4800000,
    images: [{ id: 3, image: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400", is_main: true }],
    category: { id: 3, name: "Marjonlar", slug: "necklaces" },
    metal_type: "gold",
    weight: 8.2,
    in_stock: true,
    is_featured: true,
    created_at: "2024-01-03",
  },
  {
    id: 4,
    name: "Bilaguzuk, oltin 585",
    description: "Zamonaviy dizayn",
    price: 3100000,
    images: [{ id: 4, image: "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400", is_main: true }],
    category: { id: 4, name: "Bilaguzuklar", slug: "bracelets" },
    metal_type: "gold",
    weight: 5.4,
    in_stock: false,
    is_featured: false,
    created_at: "2024-01-04",
  },
];

export function HomePage() {
  const [selectedCategory, setSelectedCategory] = useState<string>();
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { hapticFeedback } = useTelegram();
  const addItem = useCartStore((state) => state.addItem);
  const openCart = useCartStore((state) => state.openCart);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setProducts(MOCK_PRODUCTS);
      setIsLoading(false);
    }, 1000);
  }, []);

  const filteredProducts = selectedCategory
    ? products.filter((p) => p.category.slug === selectedCategory)
    : products;

  const handleAddToCart = (product: Product) => {
    addItem(product);
    hapticFeedback.impactOccurred("medium");
  };

  const handleProductPress = (product: Product) => {
    hapticFeedback.impactOccurred("light");
    // TODO: Navigate to product detail
    console.log("Navigate to product:", product.id);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header onCartClick={openCart} />

      {/* Hero Banner */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="relative h-40 bg-gradient-to-r from-amber-100 to-amber-50 dark:from-amber-900/20 dark:to-background overflow-hidden"
      >
        <div className="absolute inset-0 flex items-center px-6">
          <div>
            <h2 className="text-2xl font-display font-bold mb-1">
              Yangi <span className="gold-text">Kolleksiya</span>
            </h2>
            <p className="text-sm text-muted-foreground">
              Premium zargarlik buyumlari
            </p>
          </div>
        </div>
        <div className="absolute right-0 bottom-0 w-32 h-32 opacity-20">
          <span className="text-8xl">💎</span>
        </div>
      </motion.div>

      {/* Categories */}
      <CategorySlider
        categories={MOCK_CATEGORIES}
        selectedCategory={selectedCategory}
        onSelect={(cat) => setSelectedCategory(cat?.slug)}
      />

      {/* Products Grid */}
      <div className="px-4 pb-20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold">
            {selectedCategory
              ? MOCK_CATEGORIES.find((c) => c.slug === selectedCategory)?.name
              : "Barcha mahsulotlar"}
          </h3>
          <span className="text-sm text-muted-foreground">
            {filteredProducts.length} ta
          </span>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-2 gap-3">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="space-y-2">
                <Skeleton className="aspect-square rounded-xl" />
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </div>
            ))}
          </div>
        ) : (
          <motion.div
            className="grid grid-cols-2 gap-3"
            initial="hidden"
            animate="visible"
            variants={{
              visible: {
                transition: { staggerChildren: 0.1 },
              },
            }}
          >
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onPress={handleProductPress}
                onAddToCart={handleAddToCart}
              />
            ))}
          </motion.div>
        )}

        {!isLoading && filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Mahsulot topilmadi</p>
          </div>
        )}
      </div>
    </div>
  );
}
