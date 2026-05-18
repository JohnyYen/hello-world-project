import { Skeleton } from "@/components/ui/skeleton";

export default function CursosLoading() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      <div className="bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-600 py-10 px-6 md:px-12">
        <Skeleton className="h-8 w-48 bg-white/20" />
        <Skeleton className="h-4 w-96 mt-2 bg-white/20" />
      </div>
      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8">
        <div className="flex justify-between mb-6">
          <Skeleton className="h-10 w-32" />
          <Skeleton className="h-10 w-40" />
        </div>
        <Skeleton className="h-96 w-full rounded-xl" />
      </div>
    </div>
  );
}
