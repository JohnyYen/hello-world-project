export default function DashboardLoading() {
  return (
    <div className="space-y-6">
      {/* Stats cards skeleton */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="rounded-lg border p-6 space-y-3">
            <div className="h-4 w-24 animate-pulse rounded-md bg-muted" />
            <div className="h-8 w-16 animate-pulse rounded-lg bg-muted" />
            <div className="h-3 w-32 animate-pulse rounded-md bg-muted" />
          </div>
        ))}
      </div>

      {/* Charts skeleton */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border p-6">
          <div className="h-6 w-32 animate-pulse rounded-md bg-muted mb-4" />
          <div className="h-64 animate-pulse rounded-lg bg-muted" />
        </div>
        <div className="rounded-lg border p-6">
          <div className="h-6 w-32 animate-pulse rounded-md bg-muted mb-4" />
          <div className="h-64 animate-pulse rounded-lg bg-muted" />
        </div>
      </div>
    </div>
  );
}