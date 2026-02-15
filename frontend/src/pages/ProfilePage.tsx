import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  Package,
  ChevronRight,
  LogOut,
  Settings,
  HelpCircle,
  Clock,
  CheckCircle,
  Truck,
  XCircle,
  ShoppingBag,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Skeleton } from "../components/ui/skeleton";
import { BottomNav } from "../components/BottomNav";
import { CartSheet } from "../components/CartSheet";
import { useTelegram } from "../hooks/useTelegram";
import { getOrders } from "../lib/api/orders";
import { formatPrice } from "../lib/utils";
import type { Order, OrderStatus } from "../types";

const STATUS_CONFIG: Record<
  OrderStatus,
  { label: string; icon: typeof Clock; color: string }
> = {
  pending: { label: "Kutilmoqda", icon: Clock, color: "text-yellow-500" },
  confirmed: { label: "Tasdiqlandi", icon: CheckCircle, color: "text-blue-500" },
  processing: { label: "Tayyorlanmoqda", icon: Package, color: "text-purple-500" },
  shipped: { label: "Yo'lda", icon: Truck, color: "text-indigo-500" },
  delivered: { label: "Yetkazildi", icon: CheckCircle, color: "text-green-500" },
  cancelled: { label: "Bekor qilindi", icon: XCircle, color: "text-red-500" },
};

export function ProfilePage() {
  const navigate = useNavigate();
  const [cartOpen, setCartOpen] = useState(false);
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeSection, setActiveSection] = useState<"orders" | "settings">("orders");
  const [showProfile, setShowProfile] = useState(false);
  const [showHelp, setShowHelp] = useState(false);

  const { user, hapticFeedback, close: closeTelegram } = useTelegram();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("uz-UZ", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Profile Header */}
      <div className="bg-gradient-to-br from-primary/10 to-primary/5 px-4 pt-8 pb-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full gold-gradient flex items-center justify-center text-white text-2xl font-bold shadow-lg">
            {user?.first_name?.[0] || "?"}
          </div>
          <div>
            <h1 className="text-xl font-bold">
              {user?.first_name || "Mehmon"} {user?.last_name || ""}
            </h1>
            {user?.username && (
              <p className="text-muted-foreground">@{user.username}</p>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3 mt-6">
          <div className="bg-background/80 backdrop-blur rounded-xl p-3 text-center">
            <p className="text-2xl font-bold text-primary">{orders.length}</p>
            <p className="text-xs text-muted-foreground">Buyurtmalar</p>
          </div>
          <div className="bg-background/80 backdrop-blur rounded-xl p-3 text-center">
            <p className="text-2xl font-bold text-primary">
              {orders.filter((o) => o.status === "delivered").length}
            </p>
            <p className="text-xs text-muted-foreground">Yetkazilgan</p>
          </div>
          <div className="bg-background/80 backdrop-blur rounded-xl p-3 text-center">
            <p className="text-2xl font-bold text-primary">
              {orders.filter((o) => o.status === "pending" || o.status === "processing").length}
            </p>
            <p className="text-xs text-muted-foreground">Faol</p>
          </div>
        </div>
      </div>

      {/* Section Tabs */}
      <div className="flex gap-2 px-4 py-3 border-b border-border/50">
        <Button
          variant={activeSection === "orders" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveSection("orders")}
          className={activeSection === "orders" ? "gold-gradient" : ""}
        >
          <Package className="w-4 h-4 mr-2" />
          Buyurtmalarim
        </Button>
        <Button
          variant={activeSection === "settings" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveSection("settings")}
          className={activeSection === "settings" ? "gold-gradient" : ""}
        >
          <Settings className="w-4 h-4 mr-2" />
          Sozlamalar
        </Button>
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        {activeSection === "orders" ? (
          <motion.div
            key="orders"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="px-4 py-4"
          >
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-24 w-full rounded-xl" />
                ))}
              </div>
            ) : orders.length === 0 ? (
              <div className="text-center py-16">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", damping: 15 }}
                  className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mx-auto mb-4"
                >
                  <Package className="w-10 h-10 text-muted-foreground" />
                </motion.div>
                <h3 className="font-semibold mb-2">Buyurtmalar yo'q</h3>
                <p className="text-sm text-muted-foreground mb-6">
                  Birinchi buyurtmangizni bering
                </p>
                <Button onClick={() => navigate("/")} className="gold-gradient">
                  <ShoppingBag className="w-4 h-4 mr-2" />
                  Xarid qilish
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                {orders.map((order) => {
                  const status = STATUS_CONFIG[order.status];
                  const StatusIcon = status.icon;
                  return (
                    <motion.div
                      key={order.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-muted/50 rounded-xl p-4"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <p className="font-semibold">
                            Buyurtma #{order.id}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {formatDate(order.created_at)}
                          </p>
                        </div>
                        <Badge
                          variant="secondary"
                          className={`${status.color} bg-transparent`}
                        >
                          <StatusIcon className="w-3 h-3 mr-1" />
                          {status.label}
                        </Badge>
                      </div>

                      <div className="flex items-center gap-2 mb-3 overflow-x-auto">
                        {order.items.slice(0, 4).map((item) => (
                          <img
                            key={item.id}
                            src={
                              item.product.images[0]?.image ||
                              "/placeholder.jpg"
                            }
                            alt={item.product.name}
                            className="w-12 h-12 rounded-lg object-cover shrink-0"
                          />
                        ))}
                        {order.items.length > 4 && (
                          <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center text-sm font-medium shrink-0">
                            +{order.items.length - 4}
                          </div>
                        )}
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-muted-foreground">
                          {order.items.length} ta mahsulot
                        </span>
                        <span className="font-semibold text-primary">
                          {formatPrice(order.total)}
                        </span>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="settings"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="px-4 py-4 space-y-2"
          >
            {/* Profil ma'lumotlari */}
            <button
              onClick={() => setShowProfile(!showProfile)}
              className="w-full flex items-center justify-between p-4 bg-muted/50 rounded-xl hover:bg-muted transition-colors"
            >
              <div className="flex items-center gap-3">
                <User className="w-5 h-5 text-muted-foreground" />
                <span className="font-medium">Profil ma'lumotlari</span>
              </div>
              <ChevronRight className={`w-5 h-5 text-muted-foreground transition-transform ${showProfile ? "rotate-90" : ""}`} />
            </button>
            <AnimatePresence>
              {showProfile && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="bg-muted/30 rounded-xl p-4 space-y-3">
                    <div>
                      <p className="text-xs text-muted-foreground mb-1">Ism</p>
                      <p className="font-medium">{user?.first_name || "—"} {user?.last_name || ""}</p>
                    </div>
                    {user?.username && (
                      <div>
                        <p className="text-xs text-muted-foreground mb-1">Username</p>
                        <p className="font-medium">@{user.username}</p>
                      </div>
                    )}
                    <div>
                      <p className="text-xs text-muted-foreground mb-1">Telegram ID</p>
                      <p className="font-medium font-mono">{user?.id || "—"}</p>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Yordam */}
            <button
              onClick={() => setShowHelp(!showHelp)}
              className="w-full flex items-center justify-between p-4 bg-muted/50 rounded-xl hover:bg-muted transition-colors"
            >
              <div className="flex items-center gap-3">
                <HelpCircle className="w-5 h-5 text-muted-foreground" />
                <span className="font-medium">Yordam</span>
              </div>
              <ChevronRight className={`w-5 h-5 text-muted-foreground transition-transform ${showHelp ? "rotate-90" : ""}`} />
            </button>
            <AnimatePresence>
              {showHelp && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="bg-muted/30 rounded-xl p-4 space-y-3">
                    <div>
                      <p className="font-medium mb-1">Buyurtma qanday beraman?</p>
                      <p className="text-sm text-muted-foreground">Mahsulotni tanlang, savatga qo'shing va checkout sahifasida buyurtma bering.</p>
                    </div>
                    <div>
                      <p className="font-medium mb-1">Yetkazib berish qancha?</p>
                      <p className="text-sm text-muted-foreground">500,000 so'mdan yuqori buyurtmalarga yetkazib berish bepul. Qolganlar uchun 30,000 so'm.</p>
                    </div>
                    <div>
                      <p className="font-medium mb-1">Aloqa</p>
                      <p className="text-sm text-muted-foreground">Savollar bo'lsa, Telegram orqali bog'laning. Biz tez orada javob beramiz.</p>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <button
              onClick={() => {
                hapticFeedback?.impactOccurred?.("medium");
                closeTelegram?.();
              }}
              className="w-full flex items-center justify-between p-4 bg-red-500/10 rounded-xl hover:bg-red-500/20 transition-colors text-red-500"
            >
              <div className="flex items-center gap-3">
                <LogOut className="w-5 h-5" />
                <span className="font-medium">Chiqish</span>
              </div>
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom Navigation */}
      <BottomNav
        activeTab="profile"
        onTabChange={(tab) => {
          if (tab === "cart") setCartOpen(true);
          else if (tab === "home") navigate("/");
          else if (tab === "search") navigate("/search");
          else if (tab === "favorites") navigate("/favorites");
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
