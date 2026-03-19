"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { User } from "lucide-react";
import { TeacherProfileData } from "@/app/dashboard/account/page";

interface ProfileFormProps {
  profile: TeacherProfileData;
}

export function ProfileForm({ profile }: ProfileFormProps) {
  return (
    <Card className="border-border/50 shadow-lg shadow-primary/5">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <User className="h-5 w-5 text-primary" />
          Información Personal
        </CardTitle>
        <CardDescription>
          Actualiza tu información de perfil
        </CardDescription>
      </CardHeader>
      <div className="px-6 pb-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="name">Nombre Completo</Label>
            <Input id="name" defaultValue={profile.fullName} className="bg-muted/30" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="username">Nombre de Usuario</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">@</span>
              <Input id="username" defaultValue={profile.username} className="pl-7 bg-muted/30" />
            </div>
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="email">Correo Electrónico</Label>
            <Input id="email" type="email" defaultValue={profile.email} className="bg-muted/30" />
          </div>
        </div>
        <div className="flex justify-end">
          <Button className="bg-indigo-600 hover:bg-indigo-700">
            Guardar Cambios
          </Button>
        </div>
      </div>
    </Card>
  );
}
