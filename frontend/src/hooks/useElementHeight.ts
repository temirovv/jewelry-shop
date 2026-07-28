import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Elementning joriy balandligini kuzatadi.
 *
 * `position: fixed` panel ostida kontent qolib ketmasligi uchun sahifaga
 * qancha `padding-bottom` kerakligini aniqlashda ishlatiladi. Panel balandligi
 * kontentga (masalan yetkazib berish narxi qatori) va qurilmaning safe-area
 * inset'iga qarab o'zgaradi, shuning uchun statik Tailwind qiymati yetarli emas.
 */
export function useElementHeight<T extends HTMLElement>() {
  const [height, setHeight] = useState(0);
  const observerRef = useRef<ResizeObserver | null>(null);

  const ref = useCallback((node: T | null) => {
    observerRef.current?.disconnect();

    if (!node) {
      setHeight(0);
      return;
    }

    setHeight(node.getBoundingClientRect().height);

    if (typeof ResizeObserver === "undefined") return;

    // contentRect padding'ni hisobga olmaydi — panelda p-4 va safe-area
    // inset bor, shuning uchun border-box balandligi kerak.
    observerRef.current = new ResizeObserver(() => {
      setHeight(node.getBoundingClientRect().height);
    });
    observerRef.current.observe(node);
  }, []);

  useEffect(() => () => observerRef.current?.disconnect(), []);

  return { ref, height };
}
