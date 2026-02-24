import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle } from "lucide-react";

export function FeaturesSection() {
  const features = [
    {
      title: "Ruta de Aprendizaje Adaptativa",
      description: "La plataforma ajusta la dificultad según el rendimiento del estudiante y su ritmo de aprendizaje.",
      badge: "Adaptativa"
    },
    {
      title: "Narrativa Atractiva",
      description: "Historias inmersivas que hacen que los conceptos de programación sean comprensibles y memorables.",
      badge: "Atractiva"
    },
    {
      title: "Retroalimentación Personalizada",
      description: "Comentarios personalizados en tiempo real adaptados al estilo de aprendizaje de cada estudiante.",
      badge: "Personalizada"
    },
    {
      title: "Supervisión Docente",
      description: "Paneles completos para que los educadores monitoreen el progreso de los estudiantes.",
      badge: "Supervisada"
    },
    {
      title: "Desafíos Interactivos",
      description: "Ejercicios basados en juegos que enseñan conceptos de programación a través del juego.",
      badge: "Interactiva"
    },
    {
      title: "Seguimiento de Progreso",
      description: "Análisis detallados que muestran el desarrollo de habilidades y los hitos del aprendizaje.",
      badge: "Rastreada"
    }
  ];

  const benefits = [
    "Experiencia de aprendizaje personalizada",
    "Aumento de la participación estudiantil",
    "Retroalimentación inmediata sobre el rendimiento",
    "Supervisión y conocimientos del docente",
    "Entorno de aprendizaje gamificado"
  ];

  return (
    <section id="features" className="w-full py-12 md:py-24 lg:py-32 flex flex-col align-center justify-center items-center ">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Características del Aprendizaje Basado en Juegos
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Herramientas innovadoras diseñadas para hacer que la educación en programación sea atractiva y efectiva
            </p>
          </div>
        </div>
        <div className="mx-auto grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 mt-12">
          {features.map((feature, index) => (
            <Card key={index}>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <CardTitle>{feature.title}</CardTitle>
                  <Badge variant="secondary">{feature.badge}</Badge>
                </div>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-2">
                  {benefits.map((benefit, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className="text-sm">{benefit}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="mt-20">
          <h3 className="text-2xl font-bold tracking-tighter sm:text-3xl md:text-4xl text-center mb-12">
            Por Qué Elegir Nuestra Plataforma
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card>
              <CardHeader>
                <CardTitle>Para Estudiantes</CardTitle>
                <CardDescription>Educación en programación atractiva a través de juegos</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Desafíos interactivos de programación</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Rutas de aprendizaje personalizadas</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Lecciones basadas en narrativas atractivas</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Para Docentes</CardTitle>
                <CardDescription>Monitorear y guiar el progreso del estudiante</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Paneles de progreso en tiempo real</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Análisis de rendimiento e información</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Asignaciones de aprendizaje personalizables</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}