"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LoadingState } from "@/components/ui/loading-state";
import { ResponsivePagination } from "@/components/ui/responsive-pagination";
import {
  Star,
  MessageSquare,
  Calendar,
  User,
  AlertCircle,
} from "lucide-react";
import { statisticsService } from "@/services/statistics";
import type { FeedbackHistoryItem } from "@/types/student.interface";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 10;

// Spanish strings (hardcoded — this branch does not include the i18n layer).
const STRINGS = {
  title: "Historial de feedback",
  loading: "Cargando historial de feedback...",
  error: "Error al cargar el historial de feedback",
  empty: "No hay feedback registrado para este estudiante",
  total: (n: number): string => `Mostrando ${n} registro${n === 1 ? "" : "s"}`,
  types: {
    advice: "Consejo",
    hint: "Pista",
    tip: "Sugerencia",
    message: "Mensaje",
  },
} as const;

const LOCALE = "es-ES";

const FEEDBACK_TYPE_VARIANTS: Record<string, string> = {
  advice: "bg-blue-100 text-blue-800 border-blue-200",
  hint: "bg-purple-100 text-purple-800 border-purple-200",
  tip: "bg-green-100 text-green-800 border-green-200",
  message: "bg-gray-100 text-gray-800 border-gray-200",
};

interface StudentFeedbackHistoryProps {
  studentId: string;
}

export function StudentFeedbackHistory({ studentId }: StudentFeedbackHistoryProps) {
  const [feedbackItems, setFeedbackItems] = useState<FeedbackHistoryItem[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  useEffect(() => {
    let cancelled = false;

    const fetchFeedback = async (page: number): Promise<void> => {
      setIsLoading(true);
      setError(null);

      try {
        const skip = (page - 1) * PAGE_SIZE;
        const response = await statisticsService.getStudentFeedbackHistory(studentId, {
          skip,
          limit: PAGE_SIZE,
        });
        if (cancelled) return;
        setFeedbackItems(response.items);
        setTotal(response.total);
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : STRINGS.error);
        setFeedbackItems([]);
        setTotal(0);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    void fetchFeedback(currentPage);

    return () => {
      cancelled = true;
    };
  }, [currentPage, studentId]);

  const handlePageChange = (page: number): void => {
    setCurrentPage(page);
  };

  const formatDate = (dateStr: string): string => {
    return new Date(dateStr).toLocaleDateString(LOCALE, {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const renderStars = (rating: number | null) => {
    const maxStars = 5;
    const value = rating ?? 0;

    return (
      <div className="flex items-center gap-0.5">
        {Array.from({ length: maxStars }).map((_, i) => (
          <Star
            key={i}
            className={cn(
              "h-4 w-4",
              i < value
                ? "fill-yellow-400 text-yellow-400"
                : "fill-gray-200 text-gray-300"
            )}
          />
        ))}
        {rating !== null && (
          <span className="text-sm text-muted-foreground ml-1">{rating}/5</span>
        )}
      </div>
    );
  };

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">{STRINGS.title}</CardTitle>
        </CardHeader>
        <CardContent>
          <LoadingState message={STRINGS.loading} />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">{STRINGS.title}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2 text-red-600">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">{STRINGS.title}</CardTitle>
      </CardHeader>
      <CardContent>
        {feedbackItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center text-muted-foreground">
            <MessageSquare className="h-12 w-12 mb-3 opacity-40" />
            <p className="text-lg font-medium">{STRINGS.empty}</p>
          </div>
        ) : (
          <div className="space-y-4">
            {feedbackItems.map((item) => (
              <div
                key={item.id}
                className="border rounded-lg p-4 space-y-3"
              >
                <div className="flex items-center justify-between">
                  {renderStars(item.rating)}
                  <Badge
                    className={cn(
                      "text-xs",
                      FEEDBACK_TYPE_VARIANTS[item.feedback_type] || "bg-gray-100 text-gray-800"
                    )}
                  >
                    {STRINGS.types[item.feedback_type as keyof typeof STRINGS.types] || item.feedback_type}
                  </Badge>
                </div>

                <p className="text-sm whitespace-pre-wrap">{item.comments}</p>

                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-3.5 w-3.5" />
                    {formatDate(item.created_at)}
                  </div>
                  <div className="flex items-center gap-1">
                    <User className="h-3.5 w-3.5" />
                    {item.professor_id.slice(0, 8)}...
                  </div>
                </div>
              </div>
            ))}

            {totalPages > 1 && (
              <ResponsivePagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            )}

            <p className="text-xs text-muted-foreground text-center">
              {STRINGS.total(total)}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
