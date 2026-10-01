import { motion } from "framer-motion";
import { Send } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";
import { useLocation } from "react-router-dom";
import { ZiyoraMark } from "./ZiyoraLogo";
import { buttonVariants } from "./ui/button-variants";
import { cn } from "../lib/utils";
import { springs } from "../lib/animations";
import { BOT_USERNAME, telegramAppLink } from "../lib/telegram-link";

/**
 * Sayt brauzerda (Telegram'dan tashqarida) ochilganda ko'rsatiladi.
 * Savat va buyurtma Telegram login'siz ishlamaydi, shuning uchun do'kon
 * o'rniga Mini App'ni ochishga undaymiz. Joriy sahifa (masalan ulashilgan
 * mahsulot) havolaga qo'shiladi va Telegram'da aynan o'sha sahifa ochiladi.
 */
export function OpenInTelegram() {
  const location = useLocation();
  const link = telegramAppLink(location.pathname + location.search);
  const isProduct = location.pathname.startsWith("/product/");

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-10">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={springs.bouncy}
        className="w-full max-w-sm text-center"
      >
        <div className="mx-auto mb-6 w-20 h-20 rounded-full gold-gradient flex items-center justify-center shadow-lg text-white">
          <ZiyoraMark className="w-10 h-10" variant="solid" />
        </div>

        <h1 className="text-2xl font-bold mb-2 gold-text">ZIYORA</h1>
        <p className="text-muted-foreground mb-8 leading-relaxed">
          {isProduct
            ? "Bu mahsulotni ko'rish va buyurtma berish uchun do'konimizni Telegram'da oching."
            : "Do'konimiz Telegram ichida ishlaydi. Xarid qilish uchun uni Telegram'da oching."}
        </p>

        <a
          href={link}
          className={cn(
            buttonVariants({ size: "lg" }),
            "gold-gradient w-full text-white shadow-md gap-2"
          )}
        >
          <Send className="w-5 h-5" />
          Telegram'da ochish
        </a>

        {/* Kompyuterdan kirganlar uchun — telefonda skanerlash */}
        <div className="hidden md:flex flex-col items-center mt-10">
          <div className="p-4 bg-white rounded-2xl shadow-sm border">
            <QRCodeSVG value={link} size={168} level="M" />
          </div>
          <p className="text-sm text-muted-foreground mt-3">
            Telefon kamerasi bilan skanerlang
          </p>
        </div>

        <a
          href={`https://t.me/${BOT_USERNAME}`}
          className="inline-block mt-8 text-sm text-muted-foreground hover:text-primary transition-colors"
        >
          @{BOT_USERNAME}
        </a>
      </motion.div>
    </div>
  );
}
