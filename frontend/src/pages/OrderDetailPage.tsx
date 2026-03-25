import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  PackageX,
  Clock,
  CheckCircle,
  Package,
  Truck,
  MapPin,
  Phone,
  CreditCard,
  CircleCheck,
  CircleX,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Skeleton } from "../components/ui/skeleton";
import { useTelegram } from "../hooks/useTelegram";
import { getOrder } from "../lib/api/orders";
import { formatPrice } from "../lib/utils";
import type { Order, OrderStatus } from "../types";

const STATUS_CONFIG: Record<
  OrderStatus,
  { label: string; icon: typeof Clock; color: string; bg: string }
> = {
  pending: { label: "Kutilmoqda", icon: Clock, color: "text-amber-500", bg: "bg-amber-500/10" },
  confirmed: { label: "Tasdiqlandi", icon: CircleCheck, color: "text-blue-500", bg: "bg-blue-500/10" },
  processing: { label: "Tayyorlanmoqda", icon: Package, color: "text-purple-500", bg: "bg-purple-500/10" },
  shipped: { label: "Yo'lda", icon: Truck, color: "text-indigo-500", bg: "bg-indigo-500/10" },
  delivered: { label: "Yetkazildi", icon: CircleCheck, color: "text-green-500", bg: "bg-green-500/10" },
  cancelled: { label: "Bekor qilindi", icon: CircleX, color: "text-red-500", bg: "bg-red-500/10" },
};

export function OrderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { showBackButton, hideBackButton } = useTelegram();

  useEffect(() => {
    showBackButton(() => navigate(-1));
    return () => hideBackButton();
  }, [showBackButton, hideBackButton, navigate]);

  useEffect(() => {
    const fetchOrder = async () => {
      if (!id) return;
      setIsLoading(true);
      setError(null);
      try {
        const data = await getOrder(Number(id));
        setOrder(data);
      } catch {
        setError("Buyurtma topilmadi");
      } finally {
        setIsLoading(false);
      }
    };
    fetchOrder();
  }, [id]);

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("uz-UZ", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background p-4 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-12 w-full rounded-xl" />
        <Skeleton className="h-32 w-full rounded-xl" />
        <Skeleton className="h-24 w-full rounded-xl" />
        <Skeleton className="h-24 w-full rounded-xl" />
      </div>
    );
  }

  if (error || !order) {
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
        <h2 className="text-xl font-semibold mb-2">Buyurtma topilmadi</h2>
        <p className="text-muted-foreground mb-4 text-center">{error}</p>
        <Button onClick={() => navigate(-1)}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Orqaga qaytish
        </Button>
      </div>
    );
  }

  const status = STATUS_CONFIG[order.status];
  const StatusIcon = status.icon;
  const itemsTotal = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="min-h-screen bg-background pb-8">
      {/* Header */}
      <div className="bg-gradient-to-br from-primary/10 to-primary/5 px-4 pt-6 pb-5">
        <button
          onClick={() => navigate(-1)}
          className="w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm flex items-center justify-center shadow-sm mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-xl font-bold">Buyurtma #{order.id}</h1>
            <p className="text-sm text-muted-foreground mt-1">
              {formatDate(order.created_at)}
            </p>
          </div>
          <Badge
            variant="secondary"
            className={`${status.color} ${status.bg} border-0 px-3 py-1.5`}
          >
            <StatusIcon className="w-4 h-4 mr-1.5" />
            {status.label}
          </Badge>
        </div>
      </div>

      <div className="px-4 space-y-4 mt-4">
        {/* Mahsulotlar */}
        <div className="bg-muted/50 rounded-xl p-4">
          <h3 className="font-semibold mb-3">Mahsulotlar</h3>
          <div className="space-y-3">
            {order.items.map((item) => (
              <div key={item.id} className="flex items-center gap-3">
                <img
                  src={item.product.images[0]?.image || "/placeholder.svg"}
                  alt={item.product.name}
                  className="w-14 h-14 rounded-lg object-cover shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm truncate">{item.product.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {item.quantity} x {formatPrice(item.price)}
                  </p>
                </div>
                <p className="font-semibold text-sm shrink-0">
                  {formatPrice(item.price * item.quantity)}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Yetkazish ma'lumotlari */}
        <div className="bg-muted/50 rounded-xl p-4 space-y-3">
          <h3 className="font-semibold">Yetkazish</h3>
          {order.delivery_address && (
            <div className="flex items-start gap-3">
              <MapPin className="w-4 h-4 text-muted-foreground mt-0.5 shrink-0" />
              <p className="text-sm">{order.delivery_address}</p>
            </div>
          )}
          <div className="flex items-center gap-3">
            <Phone className="w-4 h-4 text-muted-foreground shrink-0" />
            <p className="text-sm">{order.phone}</p>
          </div>
          {order.comment && (
            <p className="text-sm text-muted-foreground italic">
              Izoh: {order.comment}
            </p>
          )}
        </div>

        {/* To'lov */}
        <div className="bg-muted/50 rounded-xl p-4">
          <h3 className="font-semibold mb-3">To'lov</h3>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <CreditCard className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm">{order.payment_method_display}</span>
            </div>
            <Badge
              variant="secondary"
              className={
                order.is_paid
                  ? "text-green-500 bg-green-500/10 border-0"
                  : "text-amber-500 bg-amber-500/10 border-0"
              }
            >
              {order.is_paid ? (
                <CheckCircle className="w-3 h-3 mr-1" />
              ) : (
                <Clock className="w-3 h-3 mr-1" />
              )}
              {order.is_paid ? "To'langan" : "To'lanmagan"}
            </Badge>
          </div>
        </div>

        {/* Xulosa */}
        <div className="bg-muted/50 rounded-xl p-4 space-y-2">
          <h3 className="font-semibold mb-3">Xulosa</h3>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Mahsulotlar</span>
            <span>{formatPrice(itemsTotal)}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Yetkazish</span>
            <span>
              {order.delivery_fee > 0 ? formatPrice(order.delivery_fee) : "Bepul"}
            </span>
          </div>
          <div className="border-t border-border/50 pt-2 mt-2 flex items-center justify-between">
            <span className="font-semibold">Jami</span>
            <span className="font-bold text-lg text-primary">
              {formatPrice(order.total)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
