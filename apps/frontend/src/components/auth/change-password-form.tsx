"use client";

import { useActionState, useEffect } from "react";
import { Lock } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
} from "@/components/ui/field";
import { changePasswordAction } from "@/lib/actions";

export function ChangePasswordForm() {
  const [state, action, isPending] = useActionState(changePasswordAction, null);

  useEffect(() => {
    if (state?.success) {
      toast.success(state.message || "Contraseña actualizada exitosamente");
    } else if (state?.success === false && state.message) {
      toast.error(state.message || "Error al actualizar la contraseña");
    }
  }, [state]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Seguridad de la Cuenta</CardTitle>
        <CardDescription>
          Cambia tu contraseña y configura la seguridad de tu cuenta
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <form action={action}>
          <FieldGroup className="space-y-4">
            <Field>
              <Label htmlFor="currentPassword">Contraseña Actual</Label>
              <div className="flex items-center gap-2 mt-2">
                <Input
                  id="currentPassword"
                  name="currentPassword"
                  type="password"
                  placeholder="Ingresa tu contraseña actual"
                  required
                />
                <Button size="icon" variant="outline" type="button">
                  <Lock className="h-4 w-4" />
                </Button>
              </div>
              {state?.errors?.currentPassword && (
                <FieldDescription className="text-red-500">
                  {state.errors.currentPassword[0]}
                </FieldDescription>
              )}
            </Field>

            <Separator />

            <Field>
              <Label htmlFor="newPassword">Nueva Contraseña</Label>
              <div className="flex items-center gap-2 mt-2">
                <Input
                  id="newPassword"
                  name="newPassword"
                  type="password"
                  placeholder="Ingresa una nueva contraseña"
                  required
                />
                <Button size="icon" variant="outline" type="button">
                  <Lock className="h-4 w-4" />
                </Button>
              </div>
              {state?.errors?.newPassword && (
                <FieldDescription className="text-red-500">
                  {state.errors.newPassword[0]}
                </FieldDescription>
              )}
            </Field>

            <Field>
              <Label htmlFor="confirmPassword">Confirmar Nueva Contraseña</Label>
              <div className="flex items-center gap-2 mt-2">
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  placeholder="Confirma la nueva contraseña"
                  required
                />
                <Button size="icon" variant="outline" type="button">
                  <Lock className="h-4 w-4" />
                </Button>
              </div>
              {state?.errors?.confirmPassword && (
                <FieldDescription className="text-red-500">
                  {state.errors.confirmPassword[0]}
                </FieldDescription>
              )}
            </Field>

            {state?.errors?._form && (
              <FieldDescription className="text-red-500">
                {state.errors._form[0]}
              </FieldDescription>
            )}

            <div className="pt-4">
              <Button type="submit" disabled={isPending} className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                {isPending ? "Actualizando..." : "Actualizar Contraseña"}
              </Button>
            </div>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  );
}
