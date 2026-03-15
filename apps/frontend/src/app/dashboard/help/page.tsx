import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { HelpCircle, Mail, Phone, MessageCircle } from "lucide-react";

export default function HelpPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Background pattern */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="container mx-auto py-12 px-6 relative z-10">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400">
              <HelpCircle className="h-6 w-6" />
            </div>
            <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
              Soporte
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">
            Centro de Ayuda
          </h1>
          <p className="text-muted-foreground text-lg">
            Encuentra respuestas a tus preguntas o contacta con nuestro equipo de soporte
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Search and FAQ Section */}
          <div className="lg:col-span-2 space-y-6">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Búsqueda de Ayuda</h2>
                <p className="text-sm text-muted-foreground">Encuentra respuestas rápidamente</p>
              </div>
              <div className="p-6">
                <div className="flex gap-2">
                  <Input 
                    placeholder="Buscar en la base de conocimientos..." 
                    className="h-12"
                  />
                  <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700">Buscar</Button>
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Preguntas Frecuentes</h2>
                <p className="text-sm text-muted-foreground">Respuestas a las consultas más comunes</p>
              </div>
              <div className="p-6">
                <Accordion type="single" collapsible className="w-full">
                  <AccordionItem value="item-1">
                    <AccordionTrigger>¿Cómo cambio mi contraseña?</AccordionTrigger>
                    <AccordionContent>
                      Para cambiar tu contraseña, ve a la sección de &quot;Cuenta&quot; en el menú de perfil, 
                      selecciona &quot;Seguridad&quot; y luego haz clic en &quot;Cambiar contraseña&quot;. 
                      Sigue las instrucciones para crear una nueva contraseña segura.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-2">
                    <AccordionTrigger>¿Cómo puedo ver mi progreso?</AccordionTrigger>
                    <AccordionContent>
                      Tu progreso se puede ver en la página principal del dashboard. 
                      También puedes acceder a reportes detallados en la sección &quot;Reportes&quot; 
                      donde encontrarás visualizaciones de tu avance y desempeño.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-3">
                    <AccordionTrigger>¿Qué niveles hay disponibles?</AccordionTrigger>
                    <AccordionContent>
                      Actualmente ofrecemos 10 niveles de dificultad progresiva. 
                      Cada nivel introduce nuevos conceptos de programación y desafíos interactivos. 
                      Puedes ver tu progreso en cada nivel en la página de reportes.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-4">
                    <AccordionTrigger>¿Cómo contacto con un docente?</AccordionTrigger>
                    <AccordionContent>
                      Puedes contactar a tu docente a través del botón &quot;Contactar&quot; en la página 
                      de su perfil o en la lista de estudiantes. También puedes dejar comentarios 
                      en tus tareas que serán visibles para tu docente.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-5">
                    <AccordionTrigger>¿Qué hago si encuentro un error?</AccordionTrigger>
                    <AccordionContent>
                      Si encuentras un error técnico o un problema con la plataforma, 
                      por favor repórtalo inmediatamente usando el formulario de reporte de errores 
                      en la parte inferior de esta página. Incluye una descripción detallada 
                      del problema para ayudarnos a resolverlo rápidamente.
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Reportar un Problema</h2>
                <p className="text-sm text-muted-foreground">¿Encontraste un error o tienes una sugerencia?</p>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="text-sm font-medium">Asunto</label>
                  <Input placeholder="Breve descripción del problema" />
                </div>
                <div>
                  <label className="text-sm font-medium">Descripción</label>
                  <Textarea 
                    placeholder="Describe el problema con detalle..." 
                    rows={4}
                  />
                </div>
                <div className="flex justify-end">
                  <Button className="bg-indigo-600 hover:bg-indigo-700">Enviar Reporte</Button>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Section */}
          <div className="space-y-6">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Contacto</h2>
                <p className="text-sm text-muted-foreground">¿Necesitas ayuda inmediata?</p>
              </div>
              <div className="p-6 space-y-4">
                <Button variant="outline" className="w-full flex items-center justify-start gap-3 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  <Mail className="h-5 w-5 text-indigo-500" />
                  Soporte por Email
                  <Badge variant="secondary" className="ml-auto bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300">Respondemos en 24h</Badge>
                </Button>
                <Button variant="outline" className="w-full flex items-center justify-start gap-3 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  <MessageCircle className="h-5 w-5 text-indigo-500" />
                  Chat en Vivo
                  <Badge variant="secondary" className="ml-auto bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300">Disponible</Badge>
                </Button>
                <Button variant="outline" className="w-full flex items-center justify-start gap-3 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  <Phone className="h-5 w-5 text-indigo-500" />
                  Soporte Telefónico
                  <Badge variant="destructive" className="ml-auto">No disponible</Badge>
                </Button>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Recursos Útiles</h2>
                <p className="text-sm text-muted-foreground">Documentación y guías</p>
              </div>
              <div className="p-6 space-y-3">
                <Button variant="outline" className="w-full justify-start hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  Guía de Inicio Rápido
                </Button>
                <Button variant="outline" className="w-full justify-start hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  Documentación del Estudiante
                </Button>
                <Button variant="outline" className="w-full justify-start hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  Video Tutoriales
                </Button>
                <Button variant="outline" className="w-full justify-start hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400">
                  Comunidad de Usuarios
                </Button>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Estadísticas de Soporte</h2>
              </div>
              <div className="p-6 grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-indigo-50 dark:bg-indigo-950/30 rounded-lg border border-indigo-100 dark:border-indigo-800">
                  <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">98%</p>
                  <p className="text-xs text-muted-foreground">Satisfacción</p>
                </div>
                <div className="text-center p-3 bg-muted rounded-lg">
                  <p className="text-2xl font-bold">24h</p>
                  <p className="text-xs text-muted-foreground">Tiempo de respuesta</p>
                </div>
                <div className="text-center p-3 bg-muted rounded-lg">
                  <p className="text-2xl font-bold">500+</p>
                  <p className="text-xs text-muted-foreground">Preguntas FAQ</p>
                </div>
                <div className="text-center p-3 bg-muted rounded-lg">
                  <p className="text-2xl font-bold">24/7</p>
                  <p className="text-xs text-muted-foreground">Disponibilidad</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
