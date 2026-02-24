import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { 
  Star, 
  ThumbsUp, 
  ThumbsDown, 
  Send,
  User,
  Clock,
  TrendingUp
} from "lucide-react";
import { useNotifications } from "@/hooks/use-notifications";

interface Student {
  id: string;
  name: string;
  email: string;
  maxLevel: number;
  status: 'active' | 'inactive' | 'unregistered';
  course: string;
  progress?: number;
  averageGrade?: number;
  lastActivity?: string;
}

interface StudentFeedbackProps {
  student: Student;
  onClose: () => void;
  onSubmit: (feedback: StudentFeedback) => void;
}

interface StudentFeedback {
  studentId: string;
  rating: number;
  strengths: string;
  improvements: string;
  comments: string;
  recommendations: string[];
}

export function StudentFeedback({ student, onClose, onSubmit }: StudentFeedbackProps) {
  const [feedback, setFeedback] = useState<Partial<StudentFeedback>>({
    studentId: student.id,
    rating: 0,
    strengths: '',
    improvements: '',
    comments: '',
    recommendations: [],
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const notifications = useNotifications();

  const handleRatingChange = (rating: number) => {
    setFeedback(prev => ({ ...prev, rating }));
  };

  const handleInputChange = (field: keyof StudentFeedback, value: string | string[]) => {
    setFeedback(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!feedback.rating || feedback.rating === 0) {
      notifications.error('Por favor, selecciona una calificación');
      return;
    }

    if (!feedback.strengths || !feedback.improvements) {
      notifications.error('Por favor, completa todos los campos obligatorios');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      onSubmit(feedback as StudentFeedback);
      notifications.success(
        `Feedback enviado a ${student.name}`,
        {
          description: 'El feedback ha sido guardado exitosamente.'
        }
      );
      onClose();
    } catch (error) {
      notifications.apiError(error, 'Error al enviar feedback');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStatusBadge = () => {
    const variants = {
      active: 'bg-green-100 text-green-800 border-green-200',
      inactive: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      unregistered: 'bg-red-100 text-red-800 border-red-200',
    };
    
    const labels = {
      active: 'Activo',
      inactive: 'Inactivo',
      unregistered: 'No Registrado',
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
              <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                <User className="h-6 w-6 text-blue-600" />
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
                  Última actividad: {student.lastActivity || 'No registrada'}
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
                  Promedio: {student.averageGrade || 'N/A'}
                </span>
              </div>
            </div>

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
                        star <= (feedback.rating || 0) 
                          ? 'fill-yellow-400 text-yellow-400' 
                          : 'fill-gray-200 text-gray-300'
                      } hover:scale-110 transition-transform`}
                    />
                  </button>
                ))}
                <span className="text-sm text-muted-foreground ml-2">
                  {feedback.rating}/5
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
                value={feedback.strengths}
                onChange={(e) => handleInputChange('strengths', e.target.value)}
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
                value={feedback.improvements}
                onChange={(e) => handleInputChange('improvements', e.target.value)}
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
                value={feedback.comments}
                onChange={(e) => handleInputChange('comments', e.target.value)}
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