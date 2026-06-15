"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Camera, Loader2, X } from "lucide-react";
import { toast } from "sonner";

interface AvatarUploadButtonProps {
  currentAvatarUrl?: string | null;
  userName?: string;
}

export function AvatarUploadButton({ currentAvatarUrl, userName }: AvatarUploadButtonProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      toast.error("Solo se permiten imágenes");
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error("La imagen no puede superar los 5MB");
      return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    // Upload
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append("avatar", file);

      const response = await fetch("/api/account/upload-avatar", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || "Error al subir la imagen");
      }

      await response.json();
      toast.success("Foto de perfil actualizada exitosamente");
      window.location.reload();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Error al subir la imagen";
      toast.error(message);
      setPreviewUrl(null);
    } finally {
      setIsUploading(false);
      // Reset file input so the same file can be re-selected
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleCancelPreview = () => {
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // If we have a preview, show it
  if (previewUrl) {
    return (
      <div className="space-y-2">
        <div className="relative mx-auto w-20 h-20">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={previewUrl}
            alt="Vista previa"
            className="w-full h-full object-cover rounded-full ring-2 ring-primary/30"
          />
          {isUploading ? (
            <div className="absolute inset-0 flex items-center justify-center bg-black/40 rounded-full">
              <Loader2 className="h-6 w-6 animate-spin text-white" />
            </div>
          ) : (
            <button
              type="button"
              onClick={handleCancelPreview}
              className="absolute -top-1 -right-1 p-0.5 bg-destructive text-white rounded-full hover:bg-destructive/90 transition-colors"
            >
              <X className="h-3 w-3" />
            </button>
          )}
        </div>
        <p className="text-xs text-center text-muted-foreground">
          {isUploading ? "Subiendo imagen..." : "Procesando imagen..."}
        </p>
      </div>
    );
  }

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      <Button
        type="button"
        variant="outline"
        disabled={isUploading}
        onClick={handleClick}
        className="w-full flex items-center gap-2 hover:bg-primary/10 hover:text-primary hover:border-primary/30 transition-all"
      >
        {isUploading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            Subiendo...
          </>
        ) : (
          <>
            <Camera className="h-4 w-4" />
            Cambiar Foto
          </>
        )}
      </Button>
    </>
  );
}
