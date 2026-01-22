import { memo, useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, Sparkles } from "lucide-react";
import { Button } from "./ui/button";

interface Slide {
  id: number;
  title: string;
  subtitle: string;
  emoji: string;
  gradient: string;
}

const slides: Slide[] = [
  {
    id: 1,
    title: "Yangi Kolleksiya",
    subtitle: "Premium zargarlik buyumlari",
    emoji: "💎",
    gradient: "from-amber-100 via-amber-50 to-orange-50 dark:from-amber-900/30 dark:via-amber-800/20 dark:to-orange-900/20",
  },
  {
    id: 2,
    title: "30% Chegirma",
    subtitle: "Tanlangan mahsulotlarga",
    emoji: "🏷️",
    gradient: "from-rose-100 via-pink-50 to-fuchsia-50 dark:from-rose-900/30 dark:via-pink-800/20 dark:to-fuchsia-900/20",
  },
  {
    id: 3,
    title: "Bepul Yetkazish",
    subtitle: "500,000 so'mdan yuqori xaridlarga",
    emoji: "🚚",
    gradient: "from-emerald-100 via-teal-50 to-cyan-50 dark:from-emerald-900/30 dark:via-teal-800/20 dark:to-cyan-900/20",
  },
];

interface HeroBannerProps {
  onExplore?: () => void;
}

export const HeroBanner = memo(function HeroBanner({ onExplore }: HeroBannerProps) {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div className="relative overflow-hidden">
      <AnimatePresence mode="wait">
        <motion.div
          key={currentSlide}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.5 }}
          className={`relative h-44 md:h-56 bg-gradient-to-r ${slides[currentSlide].gradient} mx-4 rounded-2xl overflow-hidden`}
        >
          {/* Content */}
          <div className="absolute inset-0 flex items-center px-6">
            <div className="flex-1">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <h2 className="text-2xl md:text-3xl font-display font-bold mb-1">
                  {slides[currentSlide].title.split(" ").map((word, i) => (
                    <span key={i}>
                      {i === 1 ? (
                        <span className="gold-text">{word}</span>
                      ) : (
                        word
                      )}{" "}
                    </span>
                  ))}
                </h2>
                <p className="text-sm md:text-base text-muted-foreground mb-4">
                  {slides[currentSlide].subtitle}
                </p>
                <Button
                  size="sm"
                  variant="gold"
                  className="shadow-lg"
                  onClick={onExplore}
                >
                  <Sparkles className="w-4 h-4 mr-1.5" />
                  Ko'rish
                </Button>
              </motion.div>
            </div>

            {/* Emoji */}
            <motion.div
              initial={{ opacity: 0, scale: 0.5, rotate: -10 }}
              animate={{ opacity: 1, scale: 1, rotate: 0 }}
              transition={{ delay: 0.3, type: "spring" }}
              className="text-6xl md:text-8xl opacity-80"
            >
              {slides[currentSlide].emoji}
            </motion.div>
          </div>

          {/* Decorative circles */}
          <div className="absolute -right-10 -bottom-10 w-40 h-40 rounded-full bg-white/20 dark:bg-white/5" />
          <div className="absolute -right-5 -top-5 w-20 h-20 rounded-full bg-white/10 dark:bg-white/5" />
        </motion.div>
      </AnimatePresence>

      {/* Navigation Buttons */}
      <button
        onClick={prevSlide}
        className="absolute left-6 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white/80 dark:bg-black/50 backdrop-blur-sm shadow-lg flex items-center justify-center hover:bg-white transition-colors"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>
      <button
        onClick={nextSlide}
        className="absolute right-6 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white/80 dark:bg-black/50 backdrop-blur-sm shadow-lg flex items-center justify-center hover:bg-white transition-colors"
      >
        <ChevronRight className="w-4 h-4" />
      </button>

      {/* Dots */}
      <div className="flex justify-center gap-1.5 mt-3">
        {slides.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentSlide(idx)}
            className={`h-1.5 rounded-full transition-all duration-300 ${
              idx === currentSlide
                ? "w-6 gold-gradient"
                : "w-1.5 bg-muted-foreground/30"
            }`}
          />
        ))}
      </div>
    </div>
  );
});
