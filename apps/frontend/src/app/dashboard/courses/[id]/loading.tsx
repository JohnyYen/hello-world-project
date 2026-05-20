import { Skeleton } from "@/components/ui/skeleton";

export default function CursoDetailLoading() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      <div className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 py-10 px-6 md:px-12">
        <Skeleton className="h-4 w-24 bg-white/20 mb-4" />
        <Skeleton className="h-8 w-64 bg-white/20" />
        <Skeleton className="h-4 w-96 mt-2 bg-white/20" />
      </div>
      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8">
        <Skeleton className="h-32 w-full rounded-xl mb-6" />
        <div className="flex justify-between mb-4">
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-10 w-44" />
        </div>
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    </div>
  );
}
