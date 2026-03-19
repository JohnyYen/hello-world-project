"use client";

import { Button } from "@/components/ui/button";
import {
  Settings,
  Bell,
  Globe,
  Lock,
  Activity,
  Palette,
  Database,
} from "lucide-react";

interface SettingsSection {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
}

const sections: SettingsSection[] = [
  { id: "session", title: "Sesión", description: "Configuración de sesión y autenticación", icon: Activity },
  { id: "appearance", title: "Apariencia", description: "Tema, colores y visualización", icon: Palette },
  { id: "notifications", title: "Notificaciones", description: "Cómo recibes tus notificaciones", icon: Bell },
  { id: "language", title: "Idioma", description: "Idioma y preferencias regionales", icon: Globe },
  { id: "security", title: "Seguridad", description: "Protección y privacidad de tu cuenta", icon: Lock },
  { id: "integrations", title: "Integraciones", description: "Conexión con servicios externos", icon: Database },
];

interface SettingsNavigationProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

export function SettingsNavigation({ activeSection, onSectionChange }: SettingsNavigationProps) {
  return (
    <div className="sticky top-6 space-y-2">
      {sections.map((section) => {
        const IconComponent = section.icon;
        return (
          <Button
            key={section.id}
            variant={activeSection === section.id ? "secondary" : "ghost"}
            className={`w-full justify-start h-auto py-3 px-4 ${
              activeSection === section.id
                ? "bg-primary/10 text-primary border-l-2 border-primary"
                : "hover:bg-muted"
            }`}
            onClick={() => onSectionChange(section.id)}
          >
            <IconComponent className="h-4 w-4 mr-3 flex-shrink-0" />
            <div className="text-left">
              <div className="font-medium">{section.title}</div>
              <div className="text-xs text-muted-foreground hidden lg:block">{section.description}</div>
            </div>
          </Button>
        );
      })}
    </div>
  );
}