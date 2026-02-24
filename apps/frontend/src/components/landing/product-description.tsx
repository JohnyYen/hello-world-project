import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function ProductDescription() {
  return (
    <section id="description" className="w-full py-12 md:py-24 lg:py-32 bg-muted flex flex-col align-center justify-center items-center ">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Aprende Programación a través de Juegos Interactivos
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Nuestra plataforma combina la naturaleza atractiva de los videojuegos con contenido 
              educativo para hacer que el aprendizaje de conceptos de programación sea disfrutable y efectivo.
            </p>
          </div>
        </div>
        <div className="mx-auto grid max-w-5xl grid-cols-1 md:grid-cols-2 gap-8 mt-12">
          <Card>
            <CardHeader>
              <CardTitle>Enfoque de Aprendizaje Basado en Juegos</CardTitle>
              <CardDescription>
                Haciendo accesibles conceptos complejos de programación mediante desafíos interactivos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Nuestra plataforma transforma la educación tradicional de programación incorporando mecánicas de juego 
                como niveles, logros y desafíos. Los estudiantes aprenden conceptos fundamentales de programación 
                como bucles, condicionales, funciones y programación orientada a objetos a través 
                de escenarios de juego atractivos que aumentan gradualmente en complejidad.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Panel del Docente</CardTitle>
              <CardDescription>
                Herramientas completas de monitoreo para educadores
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Los educadores acceden a paneles detallados que muestran el progreso de los estudiantes, 
                métricas de rendimiento y áreas donde los estudiantes pueden necesitar apoyo adicional. 
                La plataforma proporciona análisis en tiempo real sobre la participación de los estudiantes, 
                desafíos completados y dominio de habilidades para ayudar a los docentes a personalizar la instrucción.
              </p>
            </CardContent>
          </Card>
        </div>
        
        <div className="mt-20">
          <h3 className="text-2xl font-bold tracking-tighter sm:text-3xl md:text-4xl text-center mb-8">
            Cómo Funciona
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">1. Aprender</CardTitle>
              </CardHeader>
              <CardContent>
                <p>
                  Los estudiantes interactúan con juegos educativos que introducen conceptos de programación 
                  en un entorno divertido e interactivo. Cada nivel del juego se centra en habilidades 
                  y conceptos específicos de programación.
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">2. Practicar</CardTitle>
              </CardHeader>
              <CardContent>
                <p>
                  Una vez introducidos los conceptos, los estudiantes aplican su conocimiento resolviendo 
                  desafíos de codificación dentro del entorno del juego, recibiendo retroalimentación inmediata 
                  para reforzar el aprendizaje.
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">3. Dominar</CardTitle>
              </CardHeader>
              <CardContent>
                <p>
                  Los estudiantes progresan a través de desafíos cada vez más complejos que se basan en 
                  habilidades previas, mientras los docentes monitorean el progreso y proporcionan 
                  apoyo guiado cuando sea necesario.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}