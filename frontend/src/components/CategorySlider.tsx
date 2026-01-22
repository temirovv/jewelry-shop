import { motion } from "framer-motion";
import { cn } from "../lib/utils";
import type { Category } from "../types";

interface CategorySliderProps {
  categories: Category[];
  selectedCategory?: string;
  onSelect?: (category: Category) => void;
}

export function CategorySlider({
  categories,
  selectedCategory,
  onSelect,
}: CategorySliderProps) {
  return (
    <div className="w-full overflow-x-auto scrollbar-hide py-3">
      <motion.div
        className="flex gap-3 px-4"
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {/* All */}
        <CategoryItem
          name="Barchasi"
          isSelected={!selectedCategory}
          onClick={() => onSelect?.(undefined as unknown as Category)}
        />

        {categories.map((category) => (
          <CategoryItem
            key={category.id}
            name={category.name}
            icon={category.icon}
            isSelected={selectedCategory === category.slug}
            onClick={() => onSelect?.(category)}
          />
        ))}
      </motion.div>
    </div>
  );
}

interface CategoryItemProps {
  name: string;
  icon?: string;
  isSelected?: boolean;
  onClick?: () => void;
}

function CategoryItem({ name, icon, isSelected, onClick }: CategoryItemProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={cn(
        "flex items-center gap-2 px-4 py-2 rounded-full whitespace-nowrap transition-all",
        "border text-sm font-medium",
        isSelected
          ? "gold-gradient text-white border-transparent shadow-md"
          : "bg-background border-border hover:border-primary/50"
      )}
    >
      {icon && <span>{icon}</span>}
      <span>{name}</span>
    </motion.button>
  );
}
