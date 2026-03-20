"use client";

import { useActionState, useEffect, useState } from "react";
import { Lock, Eye, EyeOff } from "lucide-react";
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

function PasswordInput({ 
  id, 
  name, 
  placeholder, 
  required = true 
}: { 
  id: string; 
  name: string; 
  placeholder: string; 
  required?: boolean;
}) {
  const [showPassword, setShowPassword] = useState(false);
  const [showTimer, setShowTimer] = useState<NodeJS.Timeout | null>(null);

  const handleShowPassword = () => {
    setShowPassword(true);
    
    // Limpiar timer anterior si existe
    if (showTimer) {
      clearTimeout(showTimer);
    }
    
    // Ocultar después de 3 segundos
    const timer = setTimeout(() => {
      setShowPassword(false);
    }, 3000);
    
    setShowTimer(timer);
  };

  useEffect(() => {
    return () => {
      if (showTimer) {
        clearTimeout(showTimer);
      }
    };
  }, [showTimer]);

  return (
    <div className="flex items-center gap-2 mt-2">
      <Input
        id={id}
        name={name}
        type={showPassword ? "text" : "password"}
        placeholder={placeholder}
        required={required}
      />
      <Button 
        size="icon" 
        variant="outline" 
        type="button"
        onClick={handleShowPassword}
        className="shrink-0"
      >
        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
      </Button>
    </div>
  );
}

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
              <PasswordInput
                id="currentPassword"
                name="currentPassword"
                placeholder="Ingresa tu contraseña actual"
              />
              {state?.errors?.currentPassword && (
                <FieldDescription className="text-red-500">
                  {state.errors.currentPassword[0]}
                </FieldDescription>
              )}
            </Field>

            <Separator />

            <Field>
              <Label htmlFor="newPassword">Nueva Contraseña</Label>
              <PasswordInput
                id="newPassword"
                name="newPassword"
                placeholder="Ingresa una nueva contraseña"
              />
              {state?.errors?.newPassword && (
                <FieldDescription className="text-red-500">
                  {state.errors.newPassword[0]}
                </FieldDescription>
              )}
            </Field>

            <Field>
              <Label htmlFor="confirmPassword">Confirmar Nueva Contraseña</Label>
              <PasswordInput
                id="confirmPassword"
                name="confirmPassword"
                placeholder="Confirma la nueva contraseña"
              />
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
