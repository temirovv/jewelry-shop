import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  MapPin,
  Phone,
  MessageSquare,
  ShoppingBag,
  Loader2,
  CheckCircle,
  Package,
  Banknote,
  CreditCard,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { useCartStore } from "../stores/cartStore";
import { useTelegram } from "../hooks/useTelegram";
import { toast } from "../components/Toast";
import { createOrder, prepareOrderItems } from "../lib/api/orders";
import { formatPrice } from "../lib/utils";
import type { PaymentMethod } from "../types";

export function CheckoutPage() {
  const navigate = useNavigate();
  const items = useCartStore((state) => state.items);
  const getTotal = useCartStore((state) => state.getTotal);
  const clearCart = useCartStore((state) => state.clearCart);
  const { user, hapticFeedback, showBackButton, hideBackButton } = useTelegram();

  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [comment, setComment] = useState("");
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>("cash");
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [orderId, setOrderId] = useState<number | null>(null);

  useEffect(() => {
    showBackButton(() => navigate(-1));
    return () => hideBackButton();
  }, [showBackButton, hideBackButton, navigate]);

  useEffect(() => {
    if (items.length === 0 && !isSuccess) {
      navigate("/");
    }
  }, [items, isSuccess, navigate]);

  const total = getTotal();
  const deliveryFee = total >= 500000 ? 0 : 30000;
  const grandTotal = total + deliveryFee;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!phone.trim()) {
      toast.error("Telefon raqamingizni kiriting");
      hapticFeedback?.notificationOccurred?.("error");
      return;
    }

    if (phone.replace(/\D/g, "").length < 9) {
      toast.error("Telefon raqam noto'g'ri");
      hapticFeedback?.notificationOccurred?.("error");
      return;
    }

    setIsLoading(true);

    try {
      const order = await createOrder({
        items: prepareOrderItems(items),
        phone: phone.trim(),
        delivery_address: address.trim() || undefined,
        comment: comment.trim() || undefined,
        payment_method: paymentMethod,
      });

      setOrderId(order.id);
      setIsSuccess(true);
      clearCart();
      hapticFeedback?.notificationOccurred?.("success");
    } catch (err) {
      toast.error("Buyurtma yaratishda xatolik");
      hapticFeedback?.notificationOccurred?.("error");
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", damping: 15 }}
          className="w-24 h-24 rounded-full gold-gradient flex items-center justify-center mb-6"
        >
          <CheckCircle className="w-12 h-12 text-white" />
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-2xl font-bold mb-2"
        >
          Buyurtma qabul qilindi!
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-muted-foreground mb-2"
        >
          Buyurtma raqami: #{orderId}
        </motion.p>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="text-muted-foreground mb-8"
        >
          Tez orada siz bilan bog'lanamiz
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="flex gap-3"
        >
          <Button variant="outline" onClick={() => navigate("/profile")}>
            <Package className="w-4 h-4 mr-2" />
            Buyurtmalarim
          </Button>
          <Button onClick={() => navigate("/")} className="gold-gradient">
            Bosh sahifa
          </Button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pb-32">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div className="flex items-center gap-3 px-4 py-3">
          <button
            onClick={() => navigate(-1)}
            className="w-10 h-10 rounded-full bg-muted flex items-center justify-center"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-lg font-semibold">Buyurtmani rasmiylashtirish</h1>
        </div>
      </div>

      {/* Order Summary */}
      <div className="p-4">
        <div className="bg-muted/50 rounded-2xl p-4 mb-6">
          <h2 className="font-semibold mb-3 flex items-center gap-2">
            <ShoppingBag className="w-5 h-5" />
            Buyurtma ({items.length} ta)
          </h2>
          <div className="space-y-3 max-h-48 overflow-y-auto">
            {items.map((item) => (
              <div
                key={item.id}
                className="flex items-center gap-3 bg-background rounded-xl p-2"
              >
                <img
                  src={
                    item.product.images[0]?.image || "/placeholder.jpg"
                  }
                  alt={item.product.name}
                  className="w-14 h-14 rounded-lg object-cover"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm truncate">
                    {item.product.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {item.quantity} x {formatPrice(item.product.price)}
                  </p>
                </div>
                <span className="font-medium text-sm">
                  {formatPrice(item.product.price * item.quantity)}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 flex items-center gap-2">
              <Phone className="w-4 h-4" />
              Telefon raqam *
            </label>
            <Input
              type="tel"
              placeholder="+998 90 123 45 67"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="h-12"
            />
          </div>

          <div>
            <label className="text-sm font-medium mb-2 flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Yetkazib berish manzili
            </label>
            <Input
              placeholder="Shahar, ko'cha, uy..."
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="h-12"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Agar bo'sh qoldirsangiz, biz siz bilan bog'lanamiz
            </p>
          </div>

          <div>
            <label className="text-sm font-medium mb-2 flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              Izoh
            </label>
            <Input
              placeholder="Qo'shimcha ma'lumot..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              className="h-12"
            />
          </div>

          {/* To'lov usuli */}
          <div>
            <label className="text-sm font-medium mb-3 flex items-center gap-2">
              <Banknote className="w-4 h-4" />
              To'lov usuli
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setPaymentMethod("cash")}
                className={`p-4 rounded-xl border-2 transition-all ${
                  paymentMethod === "cash"
                    ? "border-primary bg-primary/5"
                    : "border-border bg-muted/30 hover:border-primary/50"
                }`}
              >
                <Banknote
                  className={`w-6 h-6 mx-auto mb-2 ${
                    paymentMethod === "cash" ? "text-primary" : "text-muted-foreground"
                  }`}
                />
                <p
                  className={`text-sm font-medium ${
                    paymentMethod === "cash" ? "text-primary" : ""
                  }`}
                >
                  Naqd pul
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Yetkazib berishda
                </p>
              </button>

              <button
                type="button"
                onClick={() => setPaymentMethod("transfer")}
                className={`p-4 rounded-xl border-2 transition-all ${
                  paymentMethod === "transfer"
                    ? "border-primary bg-primary/5"
                    : "border-border bg-muted/30 hover:border-primary/50"
                }`}
              >
                <CreditCard
                  className={`w-6 h-6 mx-auto mb-2 ${
                    paymentMethod === "transfer" ? "text-primary" : "text-muted-foreground"
                  }`}
                />
                <p
                  className={`text-sm font-medium ${
                    paymentMethod === "transfer" ? "text-primary" : ""
                  }`}
                >
                  Karta o'tkazma
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Oldindan to'lov
                </p>
              </button>
            </div>
          </div>

          {user && (
            <div className="bg-muted/50 rounded-xl p-3">
              <p className="text-sm text-muted-foreground">Buyurtmachi:</p>
              <p className="font-medium">
                {user.first_name} {user.last_name}
              </p>
            </div>
          )}
        </form>
      </div>

      {/* Bottom Price Bar */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-background/80 backdrop-blur-xl border-t border-border/50 safe-area-bottom">
        <div className="space-y-2 mb-4">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Mahsulotlar</span>
            <span>{formatPrice(total)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Yetkazib berish</span>
            <span className={deliveryFee === 0 ? "text-green-600" : ""}>
              {deliveryFee === 0 ? "Bepul" : formatPrice(deliveryFee)}
            </span>
          </div>
          <div className="flex justify-between font-semibold text-lg border-t border-border/50 pt-2">
            <span>Jami</span>
            <span className="text-primary">{formatPrice(grandTotal)}</span>
          </div>
        </div>

        <Button
          type="submit"
          className="w-full h-12 gold-gradient text-white font-medium rounded-xl"
          disabled={isLoading}
          onClick={handleSubmit}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Yuklanmoqda...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5 mr-2" />
              Buyurtma berish
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
