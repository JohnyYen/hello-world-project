import { HeroSection, ProductDescription, FeaturesSection, VideoSection } from "@/components/landing";

export default function Home() {
  return (
    <div className="font-sans ">
        <HeroSection />
        <ProductDescription />
        <FeaturesSection />
        <VideoSection 
          videoSrc="https://www.youtube.com/embed/9bZkp7q19f0" 
          title="Plataforma Educativa en Acción" 
          description="Descubre cómo nuestra plataforma transforma el aprendizaje de programación con herramientas intuitivas y análisis en tiempo real"
        />
    </div>
  );
}