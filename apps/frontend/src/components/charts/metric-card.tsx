import { cn } from "@/lib/utils";

interface MetricCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  className?: string;
  variant?: "default" | "highlight" | "accent";
}

export function MetricCard({
  title,
  value,
  description,
  icon,
  trend,
  className,
  variant = "default",
}: MetricCardProps) {
  const variantStyles = {
    default: "",
    highlight: "border-amber-500/30 bg-gradient-to-br from-amber-50/50 to-orange-50/30 dark:from-amber-950/30 dark:to-orange-950/20",
    accent: "border-indigo-500/30 bg-gradient-to-br from-indigo-50/50 to-violet-50/30 dark:from-indigo-950/30 dark:to-violet-950/20",
  };

  const iconBgStyles = {
    default: "bg-primary/10 text-primary",
    highlight: "bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-400",
    accent: "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-400",
  };

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-xl border bg-card p-6 shadow-sm transition-all duration-300 hover:shadow-md hover:scale-[1.02]",
        variantStyles[variant],
        className
      )}
    >
      {/* Decorative corner accent */}
      <div className="absolute top-0 right-0 w-16 h-16 opacity-5">
        <svg viewBox="0 0 100 100" className="w-full h-full fill-current">
          <path d="M100 0 L100 100 C66.667 100 0 100 0 66.667 L0 0 Z" />
        </svg>
      </div>
      
      <div className="flex items-start justify-between relative z-10">
        <div className="space-y-2">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold tracking-tight">{value}</p>
          {description && (
            <p className="text-xs text-muted-foreground/80 leading-relaxed">{description}</p>
          )}
          {trend && (
            <p
              className={cn(
                "text-xs font-semibold flex items-center gap-1",
                trend.isPositive ? "text-accent" : "text-destructive"
              )}
            >
              <span className="text-base">{trend.isPositive ? "↑" : "↓"}</span>
              {Math.abs(trend.value)}%
              <span className="font-normal text-muted-foreground">
                {trend.isPositive ? "vs semana anterior" : "vs semana anterior"}
              </span>
            </p>
          )}
        </div>
        {icon && (
          <div className={cn("p-3 rounded-xl transition-transform duration-300 hover:scale-110", iconBgStyles[variant])}>
            {icon}
          </div>
        )}
      </div>
      
      {/* Subtle bottom gradient line */}
      <div className={cn(
        "absolute bottom-0 left-0 right-0 h-0.5",
        variant === "highlight" ? "bg-gradient-to-r from-amber-400 via-orange-500 to-amber-400" :
        variant === "accent" ? "bg-gradient-to-r from-indigo-400 via-violet-500 to-indigo-400" :
        "bg-gradient-to-r from-primary/50 via-primary to-primary/50"
      )} />
    </div>
  );
}
