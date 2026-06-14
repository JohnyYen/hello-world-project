import { HelpCircle, ChevronRight, LifeBuoy, BookOpen } from "lucide-react";
import { HelpQuickGuides } from "@/components/help/help-quick-guides";
import { HelpFaq } from "@/components/help/help-faq";
import { HelpContactForm } from "@/components/help/help-contact-form";
import { HelpSystemStatus } from "@/components/help/help-system-status";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

export default function HelpPage() {
  return (
    <div className="min-h-screen">
      {/* ─────────────── HERO ─────────────── */}
      <section className="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-indigo-700 to-violet-800 dark:from-indigo-950 dark:via-indigo-900 dark:to-violet-950">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-24 -right-24 size-96 rounded-full bg-white/5 blur-3xl" />
          <div className="absolute -bottom-32 -left-32 size-80 rounded-full bg-violet-400/10 blur-3xl" />
          <div className="absolute top-1/2 left-1/4 w-px h-48 bg-gradient-to-b from-white/10 to-transparent" />
          <div className="absolute top-1/3 right-1/3 w-px h-32 bg-gradient-to-b from-white/10 to-transparent" />
        </div>

        <div className="relative mx-auto max-w-5xl px-6 py-16 sm:py-20">
          {/* Breadcrumb */}
          <div className="flex items-center gap-1.5 text-xs text-indigo-200 mb-4">
            <span>Dashboard</span>
            <ChevronRight className="size-3" />
            <span className="text-white/90 font-medium">Centro de Ayuda</span>
          </div>

          <div className="flex items-start gap-5">
            <div className="flex size-14 shrink-0 items-center justify-center rounded-2xl bg-white/15 backdrop-blur-sm ring-1 ring-white/20">
              <LifeBuoy className="size-7 text-white" />
            </div>
            <div className="min-w-0">
              <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-white">
                Centro de Ayuda
              </h1>
              <p className="mt-2 text-lg text-indigo-200 max-w-2xl">
                Todo lo que necesitás saber para usar la plataforma como docente. Encontrá guías,
                respuestas a preguntas frecuentes y canales de soporte.
              </p>
            </div>
          </div>

          {/* Quick stats bar */}
          <div className="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Guías disponibles", value: "8" },
              { label: "Preguntas frecuentes", value: "16" },
              { label: "Tiempo de respuesta", value: "~24h" },
              { label: "Satisfacción", value: "98%" },
            ].map((stat) => (
              <div
                key={stat.label}
                className="rounded-xl bg-white/10 backdrop-blur-sm px-4 py-3 text-center ring-1 ring-white/10"
              >
                <p className="text-lg font-bold text-white">{stat.value}</p>
                <p className="text-[11px] text-indigo-200/80 mt-0.5">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom wave transition */}
        <div className="absolute bottom-0 left-0 right-0 h-6 bg-gradient-to-t from-slate-50 to-transparent dark:from-slate-950" />
      </section>

      {/* ─────────────── CONTENT ─────────────── */}
      <div className="mx-auto max-w-7xl px-6 py-10">
        {/* Guías Rápidas */}
        <HelpQuickGuides />

        <Separator className="my-10" />

        {/* Two-column layout: FAQ (main) + Sidebar */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main column: FAQ */}
          <div className="lg:col-span-2">
            <HelpFaq />

            <Separator className="my-10" />

            {/* Contact form */}
            <HelpContactForm />
          </div>

          {/* Sidebar column: System Status + Resources */}
          <div className="space-y-6">
            <HelpSystemStatus />

            {/* Resources section */}
            <section>
              <div className="mb-4">
                <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                  Recursos Útiles
                </h2>
                <p className="text-sm text-muted-foreground mt-0.5">
                  Documentación y material de apoyo
                </p>
              </div>
              <div className="space-y-2">
                {[
                  {
                    title: "Guía de Inicio Rápido",
                    desc: "Primeros pasos en la plataforma",
                    icon: BookOpen,
                    color: "text-indigo-600 dark:text-indigo-400 bg-indigo-100 dark:bg-indigo-900/40",
                  },
                  {
                    title: "Manual del Docente",
                    desc: "Guía completa de funciones",
                    icon: BookOpen,
                    color: "text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/40",
                  },
                  {
                    title: "Video Tutoriales",
                    desc: "Guías visuales paso a paso",
                    icon: BookOpen,
                    color: "text-violet-600 dark:text-violet-400 bg-violet-100 dark:bg-violet-900/40",
                  },
                  {
                    title: "Comunidad de Docentes",
                    desc: "Compartí experiencias y consejos",
                    icon: BookOpen,
                    color: "text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/40",
                  },
                  {
                    title: "Documentación Técnica",
                    desc: "API, integraciones y xAPI",
                    icon: BookOpen,
                    color: "text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800/60",
                  },
                ].map((resource) => (
                  <button
                    key={resource.title}
                    type="button"
                    className="flex w-full items-center gap-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 px-4 py-3 text-left text-sm hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-300 dark:hover:border-indigo-700 transition-all group"
                  >
                    <div
                      className={cn(
                        "flex size-9 shrink-0 items-center justify-center rounded-lg transition-colors",
                        resource.color
                      )}
                    >
                      <resource.icon className="size-4" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-slate-800 dark:text-slate-200 text-xs">
                        {resource.title}
                      </p>
                      <p className="text-[11px] text-muted-foreground">{resource.desc}</p>
                    </div>
                    <ChevronRight className="size-4 text-muted-foreground/50 group-hover:text-indigo-500 transition-colors" />
                  </button>
                ))}
              </div>
            </section>

            {/* Support hours card */}
            <section className="rounded-xl border border-slate-200 dark:border-slate-800 bg-gradient-to-br from-indigo-50/50 to-violet-50/50 dark:from-indigo-950/30 dark:to-violet-950/30 p-5">
              <div className="flex items-center gap-2 mb-3">
                <HelpCircle className="size-4 text-indigo-500" />
                <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                  Horarios de Soporte
                </h3>
              </div>
              <div className="space-y-2 text-xs text-muted-foreground">
                <div className="flex justify-between">
                  <span>Lunes a Viernes</span>
                  <span className="font-medium text-slate-700 dark:text-slate-300">9:00 - 18:00</span>
                </div>
                <div className="flex justify-between">
                  <span>Sábados</span>
                  <span className="font-medium text-slate-700 dark:text-slate-300">10:00 - 14:00</span>
                </div>
                <div className="flex justify-between">
                  <span>Domingos</span>
                  <span className="font-medium text-red-500">Cerrado</span>
                </div>
                <Separator className="my-2" />
                <div className="flex justify-between">
                  <span>Chat en vivo</span>
                  <span className="font-medium text-emerald-600 dark:text-emerald-400">Disponible</span>
                </div>
                <div className="flex justify-between">
                  <span>Email</span>
                  <span className="font-medium text-amber-600 dark:text-amber-400">~24h</span>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>

      {/* ─────────────── FOOTER ─────────────── */}
      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 mt-10">
        <div className="mx-auto max-w-7xl px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted-foreground">
            ¿No encontraste lo que buscabas? Escribinos a{" "}
            <a
              href="mailto:soporte@helloworld.edu"
              className="text-indigo-600 dark:text-indigo-400 hover:underline font-medium"
            >
              soporte@helloworld.edu
            </a>
          </p>
          <p className="text-xs text-muted-foreground">
            Hello World Platform v2.0 &mdash; Centro de Ayuda
          </p>
        </div>
      </footer>
    </div>
  );
}
