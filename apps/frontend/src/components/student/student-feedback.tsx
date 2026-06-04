"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Star,
  ThumbsUp,
  ThumbsDown,
  Send,
  User,
  Clock,
  TrendingUp,
} from "lucide-react";
import { useNotifications } from "@/hooks/use-notifications";
import { statisticsService, type FeedbackCreatePayload } from "@/services/statistics";
import type { Student } from "@/types";

interface CourseOption {
  id: string;
  name: string;
}

interface StudentFeedbackProps {
  student: Student;
  onClose: () => void;
  courses?: CourseOption[];
}

export function StudentFeedback({ student, onClose, courses }: StudentFeedbackProps) {
  const [rating, setRating] = useState(0);
  const [strengths, setStrengths] = useState("");
  const [improvements, setImprovements] = useState("");
  const [comments, setComments] = useState("");
  const [selectedCourseId, setSelectedCourseId] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const notifications = useNotifications();

  const handleRatingChange = (value: number) => {
    setRating(value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!rating || rating === 0) {
      notifications.error("Por favor, selecciona una calificación");
      return;
    }

    if (!strengths || !improvements) {
      notifications.error("Por favor, completa todos los campos obligatorios");
      return;
    }

    setIsSubmitting(true);

    try {
      const mappedComments = [
        `**Fortalezas:**\n${strengths}`,
        `**Áreas de mejora:**\n${improvements}`,
        comments,
      ]
        .filter(Boolean)
        .join("\n\n");

      const payload: FeedbackCreatePayload = {
        student_id: student.id,
        rating,
        feedback_type: "advice",
        display_in_game: false,
        comments: mappedComments,
      };

      if (selectedCourseId) {
        payload.course_id = selectedCourseId;
      }

      await statisticsService.submitFeedback(payload);

      notifications.success(`Feedback enviado a ${student.name}`, {
        description: "El feedback ha sido guardado exitosamente.",
      });
      onClose();
    } catch (error) {
      notifications.apiError(error, "Error al enviar feedback");
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStatusBadge = () => {
    const variants = {
      active: "bg-green-100 text-green-800 border-green-200",
      inactive: "bg-red-100 text-red-800 border-red-200",
      unregistered: "bg-orange-100 text-orange-800 border-orange-200",
    };

    const labels = {
      active: "Activo",
      inactive: "Inactivo",
      unregistered: "Pendiente",
    };

    return (
      <Badge className={variants[student.status]}>
        {labels[student.status]}
      </Badge>
    );
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <CardHeader className="border-b">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center">
                <User className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle className="text-xl">Feedback para {student.name}</CardTitle>
                <CardDescription className="flex items-center gap-2 mt-1">
                  <span>{student.email}</span>
                  {getStatusBadge()}
                </CardDescription>
              </div>
            </div>
            <Button variant="ghost" onClick={onClose} size="sm">
              ×
            </Button>
          </div>
        </CardHeader>

        <CardContent className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Student Info Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-muted/50 rounded-lg">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">
                  Última actividad: {student.lastActivity || "No registrada"}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">
                  Progreso: {student.progress || 0}%
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Star className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">
                  Promedio: {student.averageGrade || "N/A"}
                </span>
              </div>
            </div>

            {/* Course Selector */}
            {courses && courses.length > 0 && (
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  Curso
                </label>
                <Select
                  value={selectedCourseId}
                  onValueChange={setSelectedCourseId}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Seleccionar curso..." />
                  </SelectTrigger>
                  <SelectContent>
                    {courses.map((course) => (
                      <SelectItem key={course.id} value={course.id}>
                        {course.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {/* Rating */}
            <div className="space-y-2">
              <label className="text-sm font-medium flex items-center gap-2">
                Calificación General
                <span className="text-red-500">*</span>
              </label>
              <div className="flex items-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => handleRatingChange(star)}
                    className="transition-colors"
                    aria-label={`Calificación ${star} de 5`}
                  >
                    <Star
                      className={`h-8 w-8 ${
                        star <= rating
                          ? "fill-yellow-400 text-yellow-400"
                          : "fill-gray-200 text-gray-300"
                      } hover:scale-110 transition-transform`}
                    />
                  </button>
                ))}
                <span className="text-sm text-muted-foreground ml-2">
                  {rating}/5
                </span>
              </div>
            </div>

            {/* Strengths */}
            <div className="space-y-2">
              <label className="text-sm font-medium flex items-center gap-2">
                <ThumbsUp className="h-4 w-4 text-green-600" />
                Fortalezas del Estudiante
                <span className="text-red-500">*</span>
              </label>
              <Textarea
                value={strengths}
                onChange={(e) => setStrengths(e.target.value)}
                placeholder="Describe las fortalezas y habilidades destacadas del estudiante..."
                rows={4}
                required
              />
            </div>

            {/* Areas for Improvement */}
            <div className="space-y-2">
              <label className="text-sm font-medium flex items-center gap-2">
                <ThumbsDown className="h-4 w-4 text-orange-600" />
                Áreas de Mejora
                <span className="text-red-500">*</span>
              </label>
              <Textarea
                value={improvements}
                onChange={(e) => setImprovements(e.target.value)}
                placeholder="Describe las áreas donde el estudiante puede mejorar..."
                rows={4}
                required
              />
            </div>

            {/* Additional Comments */}
            <div className="space-y-2">
              <label className="text-sm font-medium">
                Comentarios Adicionales
              </label>
              <Textarea
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                placeholder="Cualquier comentario adicional o sugerencia específica..."
                rows={3}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={onClose}
                disabled={isSubmitting}
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                disabled={isSubmitting}
                className="min-w-[120px]"
              >
                {isSubmitting ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                    Enviando...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <Send className="h-4 w-4" />
                    Enviar Feedback
                  </div>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
