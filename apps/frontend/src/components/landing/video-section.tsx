import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

type VideoSectionProps = {
  videoSrc?: string;
  title?: string;
  description?: string;
};

export function VideoSection({ 
  videoSrc = "https://www.youtube.com/embed/dQw4w9WgXcQ", // Placeholder YouTube video
  title = "Visión General de la Plataforma",
  description = "Mire este video breve para ver cómo nuestra plataforma puede transformar el aprendizaje de programación"
}: VideoSectionProps) {
  return (
    <section className="w-full py-12 md:py-24 lg:py-32 flex flex-col align-center justify-center items-center ">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              {title}
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              {description}
            </p>
          </div>
        </div>
        <div className="mt-12 max-w-4xl mx-auto">
          <Card>
            <CardHeader className="p-0">
              <CardTitle className="sr-only">{title}</CardTitle>
              <CardDescription className="sr-only">{description}</CardDescription>
            </CardHeader>
            <CardContent className="p-0">
              <div className="aspect-video w-full">
                <iframe
                  src={videoSrc}
                  className="w-full h-full rounded-lg"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  title={title}
                ></iframe>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}