import { memo } from "react";
import { ChevronRight } from "lucide-react";

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const SectionHeader = memo(function SectionHeader({
  title,
  subtitle,
  actionLabel = "Ko'rish",
  onAction,
}: SectionHeaderProps) {
  return (
    <div className="flex items-end justify-between px-4 pt-6 pb-3">
      <div>
        <h2 className="text-lg font-display font-bold tracking-tight">{title}</h2>
        {subtitle && (
          <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>
        )}
      </div>
      {onAction && (
        <button
          onClick={onAction}
          className="flex items-center gap-0.5 text-sm font-medium text-primary hover:text-primary/80 transition-colors active:scale-95"
        >
          {actionLabel}
          <ChevronRight className="w-4 h-4" />
        </button>
      )}
    </div>
  );
});
