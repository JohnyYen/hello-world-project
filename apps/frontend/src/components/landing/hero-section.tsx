import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

export function HeroSection() {
  return (
    <section className="w-full py-12 md:py-24 lg:py-32 flex flex-col align-center justify-center items-center ">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center space-y-8 text-center">
          <div className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
              Aprende Programación Jugando
            </h1>
            <p className="max-w-[700px] text-muted-foreground md:text-xl">
              Una innovadora plataforma educativa que integra videojuegos educativos para el aprendizaje de programación, 
              con paneles para que los docentes monitoreen el progreso de los estudiantes.
            </p>
          </div>
          <div className="flex flex-col gap-4 sm:flex-row">
            <Button asChild size="lg">
              <Link href="/signup">
                Comenzar
              </Link>
            </Button>
            <Button variant="outline" size="lg">
              <Link href="/docs">
                Saber Más
              </Link>
            </Button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-4xl mt-12">
            <Card>
              <CardHeader>
                <CardTitle>90%</CardTitle>
                <CardDescription>Aumento de Participación</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Los estudiantes muestran una participación significativamente mayor con el aprendizaje basado en juegos en comparación con los métodos tradicionales.</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>En Tiempo Real</CardTitle>
                <CardDescription>Seguimiento de Rendimiento</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Los docentes pueden monitorear el progreso de los estudiantes e identificar brechas de aprendizaje al instante.</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>100+</CardTitle>
                <CardDescription>Juegos Educativos</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Biblioteca integral de juegos diseñados para enseñar conceptos de programación de manera efectiva.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}