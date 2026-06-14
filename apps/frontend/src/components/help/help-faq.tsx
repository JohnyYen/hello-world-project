"use client";

import { useState } from "react";
import { ChevronDown, Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";

interface FAQItem {
  question: string;
  answer: string;
  category: "cursos" | "estudiantes" | "niveles" | "reportes" | "cuenta" | "general";
}

const faqs: FAQItem[] = [
  {
    category: "cursos",
    question: "¿Cómo creo un curso y asigno estudiantes?",
    answer:
      "Andá a la sección <strong>Cursos</strong> y hacé click en <strong>Crear Curso</strong>. Completá el nombre, descripción, año lectivo y período. Una vez creado, desde la página de detalle del curso podés buscar e inscribir estudiantes usando el buscador multi-select. También podés asignar juegos al curso desde la misma pantalla.",
  },
  {
    category: "cursos",
    question: "¿Cómo asigno un juego a un curso?",
    answer:
      "Desde el detalle del curso, encontrá la sección <strong>Juegos Asignados</strong>. Usá el selector para buscar juegos disponibles y agregalos al curso. Podés asignar múltiples juegos y desasignarlos cuando sea necesario.",
  },
  {
    category: "cursos",
    question: "¿Puedo tener cursos de distintos años y períodos?",
    answer:
      "Sí. Al crear un curso definís el <strong>año lectivo</strong> y el <strong>período</strong> (ej: '2025 - Primer Semestre'). Esto te permite organizar cursos por año académico y comparar rendimiento entre períodos desde la sección de Reportes.",
  },
  {
    category: "estudiantes",
    question: "¿Cómo creo cuentas para mis estudiantes?",
    answer:
      "Andá a <strong>Estudiantes</strong> y hacé click en <strong>Crear Estudiante</strong>. Completá los datos obligatorios (nombre, apellido, email). El sistema genera automáticamente las credenciales de acceso. También podés crear estudiantes desde la página de detalle de un curso.",
  },
  {
    category: "estudiantes",
    question: "¿Cómo le doy seguimiento a un estudiante?",
    answer:
      "Hacé click en el nombre del estudiante desde la lista para ver su perfil completo. Ahí encontrás: progreso en cada juego, niveles completados, tiempo de juego, y métricas de rendimiento. También podés enviarle feedback personalizado desde la sección <strong>Enviar Feedback</strong>.",
  },
  {
    category: "estudiantes",
    question: "¿Cómo envio feedback a un estudiante?",
    answer:
      "Desde el perfil del estudiante, usá el formulario <strong>Enviar Feedback</strong>. Podés incluir un comentario, seleccionar el tipo (consejo, pista, tip, mensaje) y asignar una valoración. El feedback queda registrado y visible para el estudiante.",
  },
  {
    category: "niveles",
    question: "¿Cómo creo un nuevo nivel educativo?",
    answer:
      "Andá a <strong>Niveles → Crear Nivel</strong>. Se abre el editor completo donde podés: definir la información básica, configurar el estado inicial del juego, seleccionar los bloques de programación visual disponibles, definir acciones personalizadas, establecer reglas de ejecución, crear criterios de validación, y configurar mensajes de feedback.",
  },
  {
    category: "niveles",
    question: "¿Qué tipos de bloques puedo usar en un nivel?",
    answer:
      "El editor ofrece una variedad de bloques de programación visual: movimiento, control de flujo, variables, operadores lógicos, eventos, y más. Podés seleccionar exactamente qué bloques estarán disponibles para cada nivel, permitiendo una progresión pedagógica controlada.",
  },
  {
    category: "niveles",
    question: "¿Cómo exporto un nivel que ya diseñé?",
    answer:
      "Desde el editor, usá el botón <strong>Exportar</strong>. Podés copiar el JSON al portapapeles o descargarlo como archivo. Esto es útil para respaldar tus niveles, compartirlos con otros docentes, o importarlos en otra instancia de la plataforma.",
  },
  {
    category: "reportes",
    question: "¿Cómo veo el rendimiento general de mis cursos?",
    answer:
      "Andá a <strong>Reportes</strong>. Usá el selector de cursos para elegir uno o varios períodos. La vista te muestra: cantidad de estudiantes, tasa de finalización, promedio de calificaciones, evolución temporal, y distribución de rendimiento (alto/medio/bajo). Podés alternar entre las pestañas <strong>Resumen</strong>, <strong>Evolución</strong> y <strong>Comparación</strong>.",
  },
  {
    category: "reportes",
    question: "¿Cómo exporto los reportes a PDF?",
    answer:
      "En cualquier vista de reportes (generales o de estudiante), encontrá el botón <strong>Exportar PDF</strong>. Esto genera un documento imprimible con los gráficos y métricas actuales. Ideal para informes institucionales o reuniones con padres.",
  },
  {
    category: "reportes",
    question: "¿Qué métricas avanzadas están disponibles?",
    answer:
      "En la sección <strong>Métricas</strong> encontrás dashboards detallados: KPIs generales, progreso de estudiantes por curso, tasas de finalización por nivel, métricas de engagement, rendimiento por actividad, y un heatmap de actividad semanal.",
  },
  {
    category: "cuenta",
    question: "¿Cómo cambio mi contraseña?",
    answer:
      "Andá a tu perfil desde el menú de usuario y seleccioná <strong>Cambiar Contraseña</strong>. Ingresá tu contraseña actual y la nueva. Asegurate de usar una contraseña segura con al menos 8 caracteres, mayúsculas, minúsculas y números.",
  },
  {
    category: "cuenta",
    question: "¿Cómo configuro mis preferencias?",
    answer:
      "Andá a <strong>Configuración</strong>. Ahí podés personalizar: tema visual (claro/oscuro), frecuencia de notificaciones, idioma de la interfaz, sesión automática, tipo de gráficos, y formato de fechas. Los cambios se guardan automáticamente.",
  },
  {
    category: "general",
    question: "¿Qué hago si un estudiante no puede acceder?",
    answer:
      "Primero verificá que el estudiante esté correctamente inscrito en el curso desde la página de detalle del curso. Si el problema persiste, andá al perfil del estudiante y verificá su estado. Podés restablecer su acceso desde la sección de administración de usuarios. Si el problema técnico continúa, contactanos mediante el formulario de reporte.",
  },
  {
    category: "general",
    question: "¿La plataforma tiene integración con LMS?",
    answer:
      "Sí. La plataforma soporta integración con sistemas LMS. Desde la sección de configuración podés registrar credenciales LMS y sincronizar datos. Consultá la documentación técnica para más detalles sobre los formatos soportados (xAPI, LTI).",
  },
];

const categoryLabels: Record<string, string> = {
  cursos: "Cursos",
  estudiantes: "Estudiantes",
  niveles: "Niveles y Juegos",
  reportes: "Reportes y Métricas",
  cuenta: "Cuenta y Configuración",
  general: "General",
};

const categoryColors: Record<string, string> = {
  cursos: "bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300",
  estudiantes: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  niveles: "bg-violet-100 text-violet-700 dark:bg-violet-900/40 dark:text-violet-300",
  reportes: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  cuenta: "bg-slate-100 text-slate-700 dark:bg-slate-800/60 dark:text-slate-300",
  general: "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300",
};

export function HelpFaq() {
  const [openItem, setOpenItem] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredFaqs = faqs.filter((faq) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      faq.question.toLowerCase().includes(q) ||
      faq.answer.toLowerCase().includes(q) ||
      categoryLabels[faq.category].toLowerCase().includes(q)
    );
  });

  const grouped = filteredFaqs.reduce<Record<string, FAQItem[]>>((acc, faq) => {
    if (!acc[faq.category]) acc[faq.category] = [];
    acc[faq.category].push(faq);
    return acc;
  }, {});

  const categoryOrder = ["cursos", "estudiantes", "niveles", "reportes", "cuenta", "general"];

  const toggleItem = (value: string) => {
    setOpenItem(openItem === value ? null : value);
  };

  // Track open items as a Set internally for multi-item support
  // We use a single value approach for simplicity, but allow it to change

  return (
    <section>
      <div className="mb-5 space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            Preguntas Frecuentes
          </h2>
          <p className="text-sm text-muted-foreground mt-0.5">
            Respuestas a las consultas más comunes de docentes
          </p>
        </div>

        {/* Inline search filter */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
          <Input
            placeholder="Buscá en las preguntas frecuentes..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setOpenItem(null);
            }}
            className="pl-9 h-10 bg-white/60 dark:bg-slate-900/60"
          />
        </div>
      </div>

      {Object.keys(grouped).length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          <p className="text-sm">No encontramos preguntas que coincidan con tu búsqueda.</p>
          <p className="text-xs mt-1">Probá con otros términos o consultá nuestras guías rápidas.</p>
        </div>
      )}

      <div className="space-y-4">
        {categoryOrder
          .filter((cat) => grouped[cat])
          .map((category) => (
            <div key={category}>
              <div className="flex items-center gap-2 mb-2.5">
                <span
                  className={cn(
                    "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                    categoryColors[category]
                  )}
                >
                  {categoryLabels[category]}
                </span>
                <span className="text-xs text-muted-foreground">
                  {grouped[category].length}{" "}
                  {grouped[category].length === 1 ? "pregunta" : "preguntas"}
                </span>
              </div>

              <div className="rounded-lg border border-slate-200 dark:border-slate-800 divide-y divide-slate-100 dark:divide-slate-800 bg-white/60 dark:bg-slate-900/60">
                {grouped[category].map((faq, idx) => {
                  const itemId = `${category}-${idx}`;
                  const isOpen = openItem === itemId;

                  return (
                    <div key={itemId} className="group">
                      <button
                        type="button"
                        onClick={() => toggleItem(itemId)}
                        className="flex w-full items-center justify-between gap-2 px-5 py-3.5 text-left text-sm font-medium text-slate-800 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors"
                      >
                        <span className="flex-1 pr-4">{faq.question}</span>
                        <ChevronDown
                          className={cn(
                            "size-4 shrink-0 text-muted-foreground transition-transform duration-200",
                            isOpen && "rotate-180"
                          )}
                        />
                      </button>
                      <div
                        className={cn(
                          "overflow-hidden transition-all duration-200",
                          isOpen ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
                        )}
                      >
                        <div className="px-5 pb-4 text-sm text-muted-foreground leading-relaxed">
                          <div dangerouslySetInnerHTML={{ __html: faq.answer }} />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
      </div>
    </section>
  );
}
