"use client";

import { useActionState, useEffect } from "react";
import { toast } from "sonner";
import { Loader2, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, FieldDescription, FieldGroup } from "@/components/ui/field";
import { updateProfileAction, ActionState } from "@/lib/actions";
import { TeacherProfileData } from "@/app/dashboard/account/page";

interface ProfileFormProps {
  profile: TeacherProfileData;
}

export function ProfileForm({ profile }: ProfileFormProps) {
  const nameParts = profile.fullName.split(" ");
  const firstName = nameParts[0] || "";
  const lastName = nameParts.slice(1).join(" ") || "";

  const [state, action, isPending] = useActionState<ActionState | null, FormData>(
    updateProfileAction,
    null
  );

  useEffect(() => {
    if (state?.success) {
      toast.success(state.message || "Perfil actualizado exitosamente");
    } else if (state?.success === false && state.message) {
      toast.error(state.message);
    }
  }, [state]);

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
      <div className="px-6 pb-6">
        <form action={action}>
          <FieldGroup className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Field>
                <Label htmlFor="name">Nombre</Label>
                <Input
                  id="name"
                  name="name"
                  defaultValue={firstName}
                  placeholder="Ingresa tu nombre"
                />
                {state?.errors?.name && (
                  <FieldDescription className="text-red-500">
                    {state.errors.name[0]}
                  </FieldDescription>
                )}
              </Field>

              <Field>
                <Label htmlFor="lastname">Apellido</Label>
                <Input
                  id="lastname"
                  name="lastname"
                  defaultValue={lastName}
                  placeholder="Ingresa tu apellido"
                />
                {state?.errors?.lastname && (
                  <FieldDescription className="text-red-500">
                    {state.errors.lastname[0]}
                  </FieldDescription>
                )}
              </Field>
            </div>

            <Field>
              <Label htmlFor="username">Nombre de Usuario</Label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">@</span>
                <Input
                  id="username"
                  defaultValue={profile.username}
                  className="pl-7 bg-muted/30"
                  disabled
                />
              </div>
            </Field>

            <Field>
              <Label htmlFor="email">Correo Electrónico</Label>
              <Input
                id="email"
                name="email"
                type="email"
                defaultValue={profile.email}
                placeholder="correo@ejemplo.com"
              />
              {state?.errors?.email && (
                <FieldDescription className="text-red-500">
                  {state.errors.email[0]}
                </FieldDescription>
              )}
            </Field>

            <Field>
              <Label htmlFor="department">Departamento</Label>
              <Input
                id="department"
                name="department"
                defaultValue={profile.department}
                placeholder="Departamento o área"
              />
              {state?.errors?.department && (
                <FieldDescription className="text-red-500">
                  {state.errors.department[0]}
                </FieldDescription>
              )}
            </Field>

            <Field>
              <Label htmlFor="contactPhone">Teléfono de Contacto</Label>
              <Input
                id="contactPhone"
                name="contactPhone"
                type="tel"
                defaultValue={profile.contactPhone || ""}
                placeholder="+54 11 1234 5678"
              />
              {state?.errors?.contactPhone && (
                <FieldDescription className="text-red-500">
                  {state.errors.contactPhone[0]}
                </FieldDescription>
              )}
            </Field>

            {state?.errors?._form && (
              <FieldDescription className="text-red-500">
                {state.errors._form[0]}
              </FieldDescription>
            )}

            <div className="flex justify-end pt-4">
              <Button type="submit" disabled={isPending} className="bg-indigo-600 hover:bg-indigo-700 flex items-center gap-2">
                {isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Guardando...
                  </>
                ) : (
                  "Guardar Cambios"
                )}
              </Button>
            </div>
          </FieldGroup>
        </form>
      </div>
    </Card>
  );
}
