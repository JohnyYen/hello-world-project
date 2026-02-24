import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { HelpCircle, Mail, Phone, MessageCircle } from "lucide-react";

export default function HelpPage() {
  return (
    <div className="container mx-auto py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <HelpCircle className="h-8 w-8 text-blue-600" />
          Centro de Ayuda
        </h1>
        <p className="text-muted-foreground mt-2">
          Encuentra respuestas a tus preguntas o contacta con nuestro equipo de soporte
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Search and FAQ Section */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Búsqueda de Ayuda</CardTitle>
              <CardDescription>Encuentra respuestas rápidamente</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Input 
                  placeholder="Buscar en la base de conocimientos..." 
                  className="h-12"
                />
                <Button size="lg">Buscar</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Preguntas Frecuentes</CardTitle>
              <CardDescription>Respuestas a las consultas más comunes</CardDescription>
            </CardHeader>
            <CardContent>
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
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Reportar un Problema</CardTitle>
              <CardDescription>¿Encontraste un error o tienes una sugerencia?</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
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
                  <Button>Enviar Reporte</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Contact Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Contacto</CardTitle>
              <CardDescription>¿Necesitas ayuda inmediata?</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button variant="outline" className="w-full flex items-center justify-start gap-3">
                <Mail className="h-5 w-5" />
                Soporte por Email
                <Badge variant="secondary" className="ml-auto">Respondemos en 24h</Badge>
              </Button>
              <Button variant="outline" className="w-full flex items-center justify-start gap-3">
                <MessageCircle className="h-5 w-5" />
                Chat en Vivo
                <Badge variant="secondary" className="ml-auto">Disponible</Badge>
              </Button>
              <Button variant="outline" className="w-full flex items-center justify-start gap-3">
                <Phone className="h-5 w-5" />
                Soporte Telefónico
                <Badge variant="destructive" className="ml-auto">No disponible</Badge>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recursos Útiles</CardTitle>
              <CardDescription>Documentación y guías</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start">
                Guía de Inicio Rápido
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Documentación del Estudiante
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Video Tutoriales
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Comunidad de Usuarios
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Estadísticas de Soporte</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-muted rounded-lg">
                <p className="text-2xl font-bold">98%</p>
                <p className="text-sm text-muted-foreground">Satisfacción</p>
              </div>
              <div className="text-center p-3 bg-muted rounded-lg">
                <p className="text-2xl font-bold">24h</p>
                <p className="text-sm text-muted-foreground">Tiempo de respuesta</p>
              </div>
              <div className="text-center p-3 bg-muted rounded-lg">
                <p className="text-2xl font-bold">500+</p>
                <p className="text-sm text-muted-foreground">Preguntas FAQ</p>
              </div>
              <div className="text-center p-3 bg-muted rounded-lg">
                <p className="text-2xl font-bold">24/7</p>
                <p className="text-sm text-muted-foreground">Disponibilidad</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}