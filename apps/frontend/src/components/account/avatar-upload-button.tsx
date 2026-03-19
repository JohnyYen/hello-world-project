"use client";

import { Button } from "@/components/ui/button";
import { Camera } from "lucide-react";

export function AvatarUploadButton() {
  return (
    <Button
      variant="outline"
      className="w-full flex items-center gap-2 hover:bg-primary/10 hover:text-primary hover:border-primary/30 transition-all"
    >
      <Camera className="h-4 w-4" />
      Cambiar Foto
    </Button>
  );
}
