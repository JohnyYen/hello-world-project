import { cn } from "@/lib/utils";

interface LoadingStateProps {
  message?: string;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function LoadingState({ 
  message = "Cargando...", 
  className,
  size = "md"
}: LoadingStateProps) {
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-6 w-6", 
    lg: "h-8 w-8"
  };

  return (
    <div className={cn("flex items-center justify-center p-8", className)}>
      <div className="flex items-center space-x-3">
        <div 
          className={cn(
            "animate-spin rounded-full border-2 border-primary border-t-transparent",
            sizeClasses[size]
          )}
        />
        <span className="text-muted-foreground">{message}</span>
      </div>
    </div>
  );
}

interface SkeletonLoaderProps {
  lines?: number;
  className?: string;
}

export function SkeletonLoader({ lines = 3, className }: SkeletonLoaderProps) {
  return (
    <div className={cn("space-y-3", className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div 
          key={i}
          className="h-4 bg-muted rounded animate-pulse"
          style={{
            width: `${Math.random() * 40 + 60}%`, // Random width between 60-100%
            animationDelay: `${i * 0.1}s`
          }}
        />
      ))}
    </div>
  );
}

interface TableSkeletonProps {
  rows?: number;
  columns?: number;
  className?: string;
}

export function TableSkeleton({ 
  rows = 5, 
  columns = 4,
  className 
}: TableSkeletonProps) {
  return (
    <div className={cn("rounded-md border", className)}>
      <div className="border-b p-4">
        <div className="flex space-x-4">
          {Array.from({ length: columns }).map((_, i) => (
            <div key={i} className="h-10 w-32 animate-pulse rounded-lg bg-muted" />
          ))}
        </div>
      </div>
      <div className="divide-y">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="flex items-center space-x-4 p-4">
            <div className="h-10 w-10 animate-pulse rounded-full bg-muted" />
            {Array.from({ length: columns - 1 }).map((_, j) => (
              <div key={j} className="flex-1 space-y-2">
                <div className="h-4 w-48 animate-pulse rounded-md bg-muted" />
                <div className="h-3 w-32 animate-pulse rounded-md bg-muted" />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

interface CardSkeletonProps {
  className?: string;
  showAvatar?: boolean;
}

export function CardSkeleton({ className, showAvatar = false }: CardSkeletonProps) {
  return (
    <div className={cn("rounded-lg border p-6 space-y-4", className)}>
      {showAvatar && (
        <div className="flex items-center space-x-3">
          <div className="h-12 w-12 animate-pulse rounded-full bg-muted" />
          <div className="space-y-2">
            <div className="h-4 w-32 animate-pulse rounded-md bg-muted" />
            <div className="h-3 w-24 animate-pulse rounded-md bg-muted" />
          </div>
        </div>
      )}
      <div className="space-y-3">
        <div className="h-6 w-40 animate-pulse rounded-md bg-muted" />
        <div className="h-4 w-full animate-pulse rounded-md bg-muted" />
        <div className="h-4 w-3/4 animate-pulse rounded-md bg-muted" />
      </div>
    </div>
  );
}