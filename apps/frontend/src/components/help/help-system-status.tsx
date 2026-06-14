import { cn } from "@/lib/utils";
import { CheckCircle2, Clock, Users, Wifi, ShieldCheck, BookOpen } from "lucide-react";

interface StatusBadgeProps {
  label: string;
  status: "operational" | "degraded" | "down";
}

function StatusBadge({ label, status }: StatusBadgeProps) {
  const statusConfig = {
    operational: {
      dot: "bg-emerald-500",
      text: "Operativo",
      bg: "bg-emerald-50 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-900",
      textColor: "text-emerald-700 dark:text-emerald-300",
    },
    degraded: {
      dot: "bg-amber-500",
      text: "Degradado",
      bg: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-900",
      textColor: "text-amber-700 dark:text-amber-300",
    },
    down: {
      dot: "bg-red-500",
      text: "Caído",
      bg: "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-900",
      textColor: "text-red-700 dark:text-red-300",
    },
  };

  const config = statusConfig[status];

  return (
    <div
      className={cn(
        "flex items-center justify-between rounded-lg border px-3.5 py-2.5",
        config.bg
      )}
    >
      <span className="text-xs font-medium text-slate-700 dark:text-slate-300">{label}</span>
      <div className="flex items-center gap-1.5">
        <span className={cn("size-2 rounded-full", config.dot)} />
        <span className={cn("text-xs font-medium", config.textColor)}>{config.text}</span>
      </div>
    </div>
  );
}

const stats = [
  {
    icon: Users,
    value: "1,284",
    label: "Docentes activos",
    color: "text-indigo-600 dark:text-indigo-400",
    bg: "bg-indigo-100 dark:bg-indigo-900/40",
  },
  {
    icon: BookOpen,
    value: "156",
    label: "Cursos activos",
    color: "text-emerald-600 dark:text-emerald-400",
    bg: "bg-emerald-100 dark:bg-emerald-900/40",
  },
  {
    icon: Clock,
    value: "99.9%",
    label: "Uptime mensual",
    color: "text-violet-600 dark:text-violet-400",
    bg: "bg-violet-100 dark:bg-violet-900/40",
  },
  {
    icon: ShieldCheck,
    value: "24/7",
    label: "Monitoreo",
    color: "text-amber-600 dark:text-amber-400",
    bg: "bg-amber-100 dark:bg-amber-900/40",
  },
];

export function HelpSystemStatus() {
  return (
    <section>
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Estado del Sistema
        </h2>
        <p className="text-sm text-muted-foreground mt-0.5">
          Servicios y disponibilidad de la plataforma
        </p>
      </div>

      {/* Service statuses */}
      <div className="space-y-2 mb-5">
        <StatusBadge label="API REST" status="operational" />
        <StatusBadge label="Base de datos" status="operational" />
        <StatusBadge label="Editor de niveles" status="operational" />
        <StatusBadge label="Exportación de reportes" status="operational" />
        <StatusBadge label="WebSockets / tiempo real" status="degraded" />
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-2">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="rounded-lg border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 p-3 text-center"
          >
            <div className={cn("inline-flex items-center justify-center mb-1.5", stat.bg, "rounded-full p-1.5")}>
              <stat.icon className={cn("size-3.5", stat.color)} />
            </div>
            <p className="text-sm font-bold text-slate-900 dark:text-slate-100">{stat.value}</p>
            <p className="text-[10px] text-muted-foreground">{stat.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
