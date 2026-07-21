import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ChevronLeft, ChevronRight } from "lucide-react";
import { useTelegram } from "../hooks/useTelegram";
import type { ProductImage } from "../types";

interface ProductImageGalleryProps {
  images: ProductImage[];
  alt: string;
  className?: string;
  topOverlay?: React.ReactNode;
  bottomOverlay?: React.ReactNode;
}

const PLACEHOLDER = "/placeholder.svg";

export function ProductImageGallery({
  images,
  alt,
  className = "",
  topOverlay,
  bottomOverlay,
}: ProductImageGalleryProps) {
  const [index, setIndex] = useState(0);
  const [fullscreen, setFullscreen] = useState(false);
  const { hapticFeedback } = useTelegram();

  const count = images.length;
  const safeIndex = Math.min(index, Math.max(0, count - 1));
  const currentSrc = images[safeIndex]?.image || PLACEHOLDER;

  const next = useCallback(() => {
    if (count <= 1) return;
    setIndex((i) => (i + 1) % count);
    hapticFeedback?.selectionChanged?.();
  }, [count, hapticFeedback]);

  const prev = useCallback(() => {
    if (count <= 1) return;
    setIndex((i) => (i - 1 + count) % count);
    hapticFeedback?.selectionChanged?.();
  }, [count, hapticFeedback]);

  useEffect(() => {
    if (!fullscreen) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setFullscreen(false);
      else if (e.key === "ArrowLeft") prev();
      else if (e.key === "ArrowRight") next();
    };
    window.addEventListener("keydown", handler);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", handler);
      document.body.style.overflow = "";
    };
  }, [fullscreen, next, prev]);

  return (
    <>
      <div className={`relative aspect-square bg-muted overflow-hidden ${className}`}>
        {topOverlay}

        <AnimatePresence mode="wait">
          <motion.div
            key={safeIndex}
            drag={count > 1 ? "x" : false}
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.15}
            onDragEnd={(_, info) => {
              if (info.offset.x > 50) prev();
              else if (info.offset.x < -50) next();
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="w-full h-full cursor-zoom-in active:cursor-grabbing"
            onClick={() => setFullscreen(true)}
          >
            <img
              src={currentSrc}
              alt={alt}
              className="w-full h-full object-cover select-none"
              draggable={false}
            />
          </motion.div>
        </AnimatePresence>

        {count > 1 && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-2.5 py-1 rounded-full bg-black/40 backdrop-blur-sm text-white text-xs font-medium">
            {safeIndex + 1} / {count}
          </div>
        )}

        {count > 1 && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5 z-10">
            {images.map((_, i) => (
              <button
                key={i}
                onClick={(e) => {
                  e.stopPropagation();
                  setIndex(i);
                }}
                className={`h-2.5 rounded-full transition-all duration-300 ${
                  i === safeIndex
                    ? "w-8 gold-gradient shadow-md"
                    : "w-2.5 bg-white/60 backdrop-blur-sm"
                }`}
                aria-label={`Rasm ${i + 1}`}
              />
            ))}
          </div>
        )}

        {bottomOverlay}
      </div>

      {count > 1 && (
        <div className="flex gap-2 px-4 pt-3 overflow-x-auto scrollbar-hide">
          {images.map((img, i) => (
            <button
              key={img.id ?? i}
              onClick={() => setIndex(i)}
              className={`flex-shrink-0 w-16 h-16 rounded-xl overflow-hidden border-2 transition-all ${
                i === safeIndex
                  ? "border-primary shadow-md"
                  : "border-transparent opacity-60"
              }`}
              aria-label={`Rasm ${i + 1}`}
            >
              <img
                src={img.image || PLACEHOLDER}
                alt={`${alt} ${i + 1}`}
                className="w-full h-full object-cover"
                draggable={false}
              />
            </button>
          ))}
        </div>
      )}

      <AnimatePresence>
        {fullscreen && (
          <FullscreenViewer
            images={images}
            alt={alt}
            index={safeIndex}
            onIndexChange={setIndex}
            onClose={() => setFullscreen(false)}
          />
        )}
      </AnimatePresence>
    </>
  );
}

interface FullscreenViewerProps {
  images: ProductImage[];
  alt: string;
  index: number;
  onIndexChange: (i: number) => void;
  onClose: () => void;
}

function FullscreenViewer({
  images,
  alt,
  index,
  onIndexChange,
  onClose,
}: FullscreenViewerProps) {
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [prevIndex, setPrevIndex] = useState(index);
  const pinchStart = useRef<number | null>(null);
  const pinchStartScale = useRef(1);
  const count = images.length;
  const src = images[index]?.image || PLACEHOLDER;

  // Rasm almashganda zoom/pan holatini tiklash (render paytida — React tavsiyasi)
  if (index !== prevIndex) {
    setPrevIndex(index);
    setScale(1);
    setOffset({ x: 0, y: 0 });
  }

  const handleTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length === 2) {
      const [a, b] = [e.touches[0], e.touches[1]];
      pinchStart.current = Math.hypot(
        a.clientX - b.clientX,
        a.clientY - b.clientY,
      );
      pinchStartScale.current = scale;
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (e.touches.length === 2 && pinchStart.current) {
      const [a, b] = [e.touches[0], e.touches[1]];
      const dist = Math.hypot(
        a.clientX - b.clientX,
        a.clientY - b.clientY,
      );
      const next = (pinchStartScale.current * dist) / pinchStart.current;
      setScale(Math.max(1, Math.min(4, next)));
    }
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (e.touches.length < 2) pinchStart.current = null;
    if (scale < 1.05) {
      setScale(1);
      setOffset({ x: 0, y: 0 });
    }
  };

  const handleDoubleClick = () => {
    setScale((s) => (s > 1 ? 1 : 2));
    if (scale > 1) setOffset({ x: 0, y: 0 });
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
      className="fixed inset-0 z-[100] bg-black flex items-center justify-center"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      <button
        onClick={onClose}
        className="absolute top-4 right-4 z-10 w-11 h-11 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center text-white"
        aria-label="Yopish"
      >
        <X className="w-6 h-6" />
      </button>

      {count > 1 && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-3 py-1.5 rounded-full bg-white/10 backdrop-blur-sm text-white text-sm font-medium">
          {index + 1} / {count}
        </div>
      )}

      <motion.div
        key={index}
        drag={scale <= 1 && count > 1 ? "x" : scale > 1 ? true : false}
        dragConstraints={
          scale > 1
            ? { left: -200 * scale, right: 200 * scale, top: -200 * scale, bottom: 200 * scale }
            : { left: 0, right: 0 }
        }
        dragElastic={scale > 1 ? 0 : 0.2}
        onDragEnd={(_, info) => {
          if (scale > 1) {
            setOffset({ x: info.offset.x, y: info.offset.y });
          } else if (Math.abs(info.offset.x) > 80) {
            if (info.offset.x < 0) onIndexChange((index + 1) % count);
            else onIndexChange((index - 1 + count) % count);
          }
        }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center touch-none"
        style={{ width: "100%", height: "100%" }}
      >
        <motion.img
          src={src}
          alt={alt}
          className="max-w-full max-h-full object-contain select-none"
          animate={{ scale, x: offset.x, y: offset.y }}
          transition={{ type: "spring", stiffness: 200, damping: 25 }}
          onDoubleClick={handleDoubleClick}
          draggable={false}
        />
      </motion.div>

      {count > 1 && (
        <>
          <button
            onClick={() => onIndexChange((index - 1 + count) % count)}
            className="hidden md:flex absolute left-4 top-1/2 -translate-y-1/2 z-10 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm items-center justify-center text-white"
            aria-label="Oldingi"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
          <button
            onClick={() => onIndexChange((index + 1) % count)}
            className="hidden md:flex absolute right-4 top-1/2 -translate-y-1/2 z-10 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm items-center justify-center text-white"
            aria-label="Keyingi"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        </>
      )}
    </motion.div>
  );
}
