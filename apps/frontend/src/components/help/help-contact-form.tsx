"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Loader2, Send, Mail, MessageCircle, Clock, ChevronRight, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Field,
  FieldDescription,
  FieldGroup,
} from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface FormErrors {
  name?: string;
  email?: string;
  category?: string;
  subject?: string;
  description?: string;
}

const categories = [
  { value: "technical", label: "Problema técnico" },
  { value: "account", label: "Gestión de cuenta" },
  { value: "content", label: "Contenido educativo" },
  { value: "student", label: "Problema con estudiante" },
  { value: "feature", label: "Solicitud de funcionalidad" },
  { value: "other", label: "Otro" },
];

export function HelpContactForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);

    const name = formData.get("name") as string;
    const email = formData.get("email") as string;
    const category = formData.get("category") as string;
    const subject = formData.get("subject") as string;
    const description = formData.get("description") as string;

    // Client-side validation
    const newErrors: FormErrors = {};
    if (!name || name.trim().length < 2) {
      newErrors.name = "El nombre debe tener al menos 2 caracteres";
    }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Ingresá un email válido";
    }
    if (!category) {
      newErrors.category = "Seleccioná una categoría";
    }
    if (!subject || subject.trim().length < 5) {
      newErrors.subject = "El asunto debe tener al menos 5 caracteres";
    }
    if (!description || description.trim().length < 10) {
      newErrors.description = "La descripción debe tener al menos 10 caracteres";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) return;

    setIsSubmitting(true);

    // Simulate API call — in production this would hit a real endpoint
    await new Promise((resolve) => setTimeout(resolve, 1500));

    toast.success("Reporte enviado con éxito", {
      description: "Te responderemos a la brevedad. Gracias por ayudarnos a mejorar.",
    });

    form.reset();
    setErrors({});
    setIsSubmitting(false);
  }

  return (
    <section>
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Reportar un Problema
        </h2>
        <p className="text-sm text-muted-foreground mt-0.5">
          ¿Encontraste un error o tenés una sugerencia? Contanos
        </p>
      </div>

      <form onSubmit={handleSubmit} noValidate>
        <FieldGroup className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Field>
              <Label htmlFor="name">Nombre completo</Label>
              <Input
                id="name"
                name="name"
                placeholder="Tu nombre"
                aria-invalid={!!errors.name}
                aria-describedby={errors.name ? "name-error" : undefined}
              />
              {errors.name && (
                <p id="name-error" className="flex items-center gap-1 text-destructive text-xs mt-1" role="alert">
                  <AlertCircle className="size-3" />
                  {errors.name}
                </p>
              )}
            </Field>

            <Field>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="tu@email.com"
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? "email-error" : undefined}
              />
              {errors.email && (
                <p id="email-error" className="flex items-center gap-1 text-destructive text-xs mt-1" role="alert">
                  <AlertCircle className="size-3" />
                  {errors.email}
                </p>
              )}
            </Field>
          </div>

          <Field>
            <Label htmlFor="category">Categoría</Label>
            <Select name="category" onValueChange={() => setErrors((prev) => ({ ...prev, category: undefined }))}>
              <SelectTrigger
                id="category"
                aria-invalid={!!errors.category}
                aria-describedby={errors.category ? "category-error" : undefined}
              >
                <SelectValue placeholder="Seleccioná una categoría" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat.value} value={cat.value}>
                    {cat.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.category && (
              <p id="category-error" className="flex items-center gap-1 text-destructive text-xs mt-1" role="alert">
                <AlertCircle className="size-3" />
                {errors.category}
              </p>
            )}
          </Field>

          <Field>
            <Label htmlFor="subject">Asunto</Label>
            <Input
              id="subject"
              name="subject"
              placeholder="Describí brevemente el problema"
              aria-invalid={!!errors.subject}
              aria-describedby={errors.subject ? "subject-error" : undefined}
            />
            {errors.subject && (
              <p id="subject-error" className="flex items-center gap-1 text-destructive text-xs mt-1" role="alert">
                <AlertCircle className="size-3" />
                {errors.subject}
              </p>
            )}
          </Field>

          <Field>
            <Label htmlFor="description">Descripción</Label>
            <Textarea
              id="description"
              name="description"
              placeholder="Contanos con detalle qué pasó... ¿Qué estabas haciendo? ¿Cuándo ocurrió? ¿Podés reproducirlo?"
              rows={4}
              className="resize-y min-h-[100px]"
              aria-invalid={!!errors.description}
              aria-describedby={errors.description ? "description-error" : "description-hint"}
            />
            {errors.description ? (
              <p id="description-error" className="flex items-center gap-1 text-destructive text-xs mt-1" role="alert">
                <AlertCircle className="size-3" />
                {errors.description}
              </p>
            ) : (
              <FieldDescription id="description-hint">
                Incluí todos los detalles que puedan ayudarnos a resolver el problema más rápido.
              </FieldDescription>
            )}
          </Field>

          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Clock className="size-3.5" />
              <span>Tiempo estimado de respuesta: 24h hábiles</span>
            </div>
            <Button
              type="submit"
              disabled={isSubmitting}
              className="bg-indigo-600 hover:bg-indigo-700 text-white min-w-[140px]"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="size-4 animate-spin mr-2" />
                  Enviando...
                </>
              ) : (
                <>
                  <Send className="size-4 mr-2" />
                  Enviar Reporte
                </>
              )}
            </Button>
          </div>
        </FieldGroup>
      </form>

      {/* Quick contact options */}
      <div className="mt-6 pt-5 border-t border-slate-200 dark:border-slate-800">
        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3">
          Canales de contacto directo
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <a
            href="mailto:soporte@helloworld.edu"
            className="flex items-center gap-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 px-4 py-3 text-sm hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-300 dark:hover:border-indigo-700 transition-all group"
          >
            <Mail className="size-4 text-indigo-500 shrink-0" />
            <span className="flex-1 text-slate-700 dark:text-slate-300">soporte@helloworld.edu</span>
            <Badge
              variant="secondary"
              className="bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300 text-[10px] px-1.5 py-0"
            >
              ～24h
            </Badge>
          </a>
          <button
            type="button"
            onClick={() =>
              toast.info("Chat en vivo disponible", {
                description: "De 9:00 a 18:00h (lun-vie). En estos momentos no hay operadores disponibles.",
              })
            }
            className="flex items-center gap-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 px-4 py-3 text-sm hover:bg-emerald-50 dark:hover:bg-emerald-950/30 hover:border-emerald-300 dark:hover:border-emerald-700 transition-all group"
          >
            <MessageCircle className="size-4 text-emerald-500 shrink-0" />
            <span className="flex-1 text-slate-700 dark:text-slate-300">Chat en vivo</span>
            <Badge className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] px-1.5 py-0">
              Disponible
            </Badge>
          </button>
        </div>
      </div>
    </section>
  );
}
