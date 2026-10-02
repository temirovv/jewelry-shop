import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { Product, ProductImage } from "../types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Eski javoblarda (localStorage'dagi savat/sevimlilar) thumbnail bo'lmasligi
// mumkin — u holda asl rasm ishlatiladi
export function imageSrc(
  img: ProductImage | undefined,
  size: "thumbnail" | "large" = "thumbnail"
): string | undefined {
  if (!img) return undefined;
  return img[size] || img.image || undefined;
}

// localStorage'da saqlangan eski savat/sevimlilarda slug bo'lmasligi mumkin —
// u holda id ishlatiladi (backend raqamni id deb qabul qiladi)
export function productPath(product: Pick<Product, "id" | "slug">): string {
  return `/product/${encodeURIComponent(product.slug || String(product.id))}`;
}

export function formatPrice(price: number): string {
  return new Intl.NumberFormat("uz-UZ", {
    style: "decimal",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(price) + " so'm";
}

export function formatPriceShort(price: number): string {
  if (price >= 1000000) {
    return (price / 1000000).toFixed(1) + " mln";
  }
  if (price >= 1000) {
    return (price / 1000).toFixed(0) + " ming";
  }
  return price.toString();
}
