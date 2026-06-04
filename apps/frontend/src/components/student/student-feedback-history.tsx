"use client";

import { useState, useEffect, useCallback } from "react";
import { useTranslations, useLocale } from "next-intl";
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
  const t = useTranslations("students");
  const locale = useLocale();

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  const feedbackTypeLabels: Record<string, string> = {
    advice: t("feedbackHistory.types.advice"),
    hint: t("feedbackHistory.types.hint"),
    tip: t("feedbackHistory.types.tip"),
    message: t("feedbackHistory.types.message"),
  };

  const fetchFeedback = useCallback(async (page: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const skip = (page - 1) * PAGE_SIZE;
      const response = await statisticsService.getStudentFeedbackHistory(studentId, {
        skip,
        limit: PAGE_SIZE,
      });
      setFeedbackItems(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("feedbackHistory.error"));
      setFeedbackItems([]);
      setTotal(0);
    } finally {
      setIsLoading(false);
    }
  }, [studentId, t]);

  useEffect(() => {
    fetchFeedback(currentPage);
  }, [currentPage, fetchFeedback]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString(locale, {
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
          <CardTitle className="text-lg">{t("feedbackHistory.title")}</CardTitle>
        </CardHeader>
        <CardContent>
          <LoadingState message={t("feedbackHistory.loading")} />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">{t("feedbackHistory.title")}</CardTitle>
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
        <CardTitle className="text-lg">{t("feedbackHistory.title")}</CardTitle>
      </CardHeader>
      <CardContent>
        {feedbackItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center text-muted-foreground">
            <MessageSquare className="h-12 w-12 mb-3 opacity-40" />
            <p className="text-lg font-medium">{t("feedbackHistory.empty")}</p>
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
                    {feedbackTypeLabels[item.feedback_type] || item.feedback_type}
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
              {t("feedbackHistory.total", { total })}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
