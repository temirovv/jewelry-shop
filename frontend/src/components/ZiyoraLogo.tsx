import { memo } from "react";

interface ZiyoraMarkProps {
  className?: string;
  /** "gradient" — pushti gradient bilan to'ldirilgan; "solid" — joriy rang (currentColor) */
  variant?: "gradient" | "solid";
}

/**
 * Ziyora brend belgisi — "ziyo" (nur/yorug'lik) ma'nosiga mos uchqun (sparkle).
 * SVG, cheksiz masshtablanadi. Header, Sidebar va boshqa joylarda ishlatiladi.
 */
export const ZiyoraMark = memo(function ZiyoraMark({
  className = "w-5 h-5",
  variant = "gradient",
}: ZiyoraMarkProps) {
  const gradientId = "ziyora-mark-gradient";
  const fill = variant === "gradient" ? `url(#${gradientId})` : "currentColor";

  return (
    <svg
      viewBox="0 0 512 512"
      className={className}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      {variant === "gradient" && (
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#fb7fb8" />
            <stop offset="0.5" stopColor="#ec4899" />
            <stop offset="1" stopColor="#be185d" />
          </linearGradient>
        </defs>
      )}
      {/* Asosiy uchqun */}
      <path
        d="M256 64 Q256 256 432 256 Q256 256 256 448 Q256 256 80 256 Q256 256 256 64 Z"
        fill={fill}
      />
      {/* Kichik uchqun */}
      <path
        d="M380 104 Q380 148 428 148 Q380 148 380 192 Q380 148 332 148 Q380 148 380 104 Z"
        fill={fill}
        opacity="0.85"
      />
    </svg>
  );
});
