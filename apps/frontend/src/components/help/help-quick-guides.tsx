import {
  BookOpen,
  Users,
  GraduationCap,
  Gamepad2,
  BarChart3,
  Settings,
  MessageSquareText,
  FileText,
} from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

interface GuideCardProps {
  title: string;
  description: string;
  href: string;
  icon: React.ReactNode;
  colorClass: string;
}

function GuideCard({ title, description, href, icon, colorClass }: GuideCardProps) {
  return (
    <Link
      href={href}
      className={cn(
        "group relative overflow-hidden rounded-xl border p-5 transition-all duration-200",
        "bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm",
        "border-slate-200 dark:border-slate-800",
        "hover:shadow-lg hover:-translate-y-0.5",
        "hover:border-indigo-300 dark:hover:border-indigo-700",
        "shadow-sm"
      )}
    >
      <div className="flex items-start gap-4">
        <div
          className={cn(
            "flex size-12 shrink-0 items-center justify-center rounded-lg transition-colors duration-200",
            colorClass,
            "group-hover:scale-110 transition-transform"
          )}
        >
          {icon}
        </div>
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-sm text-slate-900 dark:text-slate-100 mb-1">
            {title}
          </h3>
          <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">
            {description}
          </p>
        </div>
      </div>
      {/* Hover accent line */}
      <div className="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-indigo-500 to-violet-500 scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
    </Link>
  );
}

const guides: GuideCardProps[] = [
  {
    title: "Panel de Control",
    description: "Visualiza el resumen general de tu actividad: estudiantes activos, niveles completados y tendencias.",
    href: "/dashboard",
    icon: <BarChart3 className="size-5 text-indigo-600 dark:text-indigo-400" />,
    colorClass: "bg-indigo-100 dark:bg-indigo-900/40",
  },
  {
    title: "Gestión de Estudiantes",
    description: "Crea, edita y administra cuentas de estudiantes. Asignalos a cursos y dales seguimiento personalizado.",
    href: "/dashboard/students",
    icon: <Users className="size-5 text-emerald-600 dark:text-emerald-400" />,
    colorClass: "bg-emerald-100 dark:bg-emerald-900/40",
  },
  {
    title: "Gestión de Cursos",
    description: "Crea cursos, inscribe estudiantes, asigna juegos y organiza el año lectivo.",
    href: "/dashboard/courses",
    icon: <GraduationCap className="size-5 text-blue-600 dark:text-blue-400" />,
    colorClass: "bg-blue-100 dark:bg-blue-900/40",
  },
  {
    title: "Creación de Niveles",
    description: "Diseñá experiencias educativas con el editor visual: bloques, validaciones, feedback y más.",
    href: "/dashboard/levels",
    icon: <Gamepad2 className="size-5 text-violet-600 dark:text-violet-400" />,
    colorClass: "bg-violet-100 dark:bg-violet-900/40",
  },
  {
    title: "Reportes y Métricas",
    description: "Analizá el rendimiento de tus cursos con gráficos, comparativas y exportación de datos.",
    href: "/dashboard/reports",
    icon: <FileText className="size-5 text-amber-600 dark:text-amber-400" />,
    colorClass: "bg-amber-100 dark:bg-amber-900/40",
  },
  {
    title: "Métricas Avanzadas",
    description: "Explorá dashboards detallados con KPIs, heatmaps de actividad y distribución de rendimiento.",
    href: "/dashboard/metrics",
    icon: <BarChart3 className="size-5 text-rose-600 dark:text-rose-400" />,
    colorClass: "bg-rose-100 dark:bg-rose-900/40",
  },
  {
    title: "Feedback a Estudiantes",
    description: "Enviale comentarios personalizados a cada estudiante con sugerencias y valoraciones.",
    href: "/dashboard/students",
    icon: <MessageSquareText className="size-5 text-cyan-600 dark:text-cyan-400" />,
    colorClass: "bg-cyan-100 dark:bg-cyan-900/40",
  },
  {
    title: "Configuración",
    description: "Personalizá tu experiencia: tema visual, notificaciones, idioma y preferencias de sesión.",
    href: "/dashboard/settings",
    icon: <Settings className="size-5 text-slate-600 dark:text-slate-400" />,
    colorClass: "bg-slate-100 dark:bg-slate-800/60",
  },
];

export function HelpQuickGuides() {
  return (
    <section>
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Guías Rápidas
        </h2>
        <p className="text-sm text-muted-foreground mt-0.5">
          Accedé directamente a las secciones principales de la plataforma
        </p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {guides.map((guide) => (
          <GuideCard key={guide.href} {...guide} />
        ))}
      </div>
    </section>
  );
}
