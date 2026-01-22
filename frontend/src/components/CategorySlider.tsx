import { memo, useRef } from "react";
import { motion } from "framer-motion";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "../lib/utils";
import type { Category } from "../types";

interface CategorySliderProps {
  categories: Category[];
  selectedCategory?: string;
  onSelect?: (slug: string | undefined) => void;
  loading?: boolean;
}

export const CategorySlider = memo(function CategorySlider({
  categories,
  selectedCategory,
  onSelect,
  loading = false,
}: CategorySliderProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      const scrollAmount = 200;
      scrollRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex gap-3 px-4 py-3 overflow-hidden">
        {[1, 2, 3, 4, 5].map((i) => (
          <div
            key={i}
            className="h-10 w-24 rounded-full bg-muted animate-pulse flex-shrink-0"
          />
        ))}
      </div>
    );
  }

  return (
    <div className="relative group">
      {/* Scroll Buttons */}
      <button
        onClick={() => scroll("left")}
        className="hidden md:flex absolute left-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 items-center justify-center rounded-full bg-background/90 shadow-lg border opacity-0 group-hover:opacity-100 transition-opacity"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>
      <button
        onClick={() => scroll("right")}
        className="hidden md:flex absolute right-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 items-center justify-center rounded-full bg-background/90 shadow-lg border opacity-0 group-hover:opacity-100 transition-opacity"
      >
        <ChevronRight className="w-4 h-4" />
      </button>

      {/* Categories */}
      <div
        ref={scrollRef}
        className="flex gap-2.5 px-4 py-3 overflow-x-auto scrollbar-hide scroll-smooth"
      >
        {/* All */}
        <CategoryChip
          name="Barchasi"
          emoji="✨"
          isSelected={!selectedCategory}
          onClick={() => onSelect?.(undefined)}
          index={0}
        />

        {categories.map((category, index) => (
          <CategoryChip
            key={category.id}
            name={category.name}
            emoji={category.icon}
            isSelected={selectedCategory === category.slug}
            onClick={() => onSelect?.(category.slug)}
            index={index + 1}
          />
        ))}
      </div>
    </div>
  );
});

interface CategoryChipProps {
  name: string;
  emoji?: string;
  isSelected?: boolean;
  onClick?: () => void;
  index: number;
}

const CategoryChip = memo(function CategoryChip({
  name,
  emoji,
  isSelected,
  onClick,
  index,
}: CategoryChipProps) {
  return (
    <motion.button
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.3,
        delay: index * 0.05,
        ease: "easeOut",
      }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={cn(
        "relative flex items-center gap-2 px-4 py-2.5 rounded-full whitespace-nowrap transition-all duration-300 text-sm font-medium flex-shrink-0",
        isSelected
          ? "gold-gradient text-white shadow-lg shadow-amber-500/25"
          : "bg-muted/80 hover:bg-muted text-foreground"
      )}
    >
      {emoji && <span className="text-base">{emoji}</span>}
      <span>{name}</span>

      {/* Selection indicator */}
      {isSelected && (
        <motion.div
          layoutId="categoryIndicator"
          className="absolute inset-0 rounded-full gold-gradient -z-10"
          transition={{ type: "spring", damping: 25, stiffness: 300 }}
        />
      )}
    </motion.button>
  );
});
